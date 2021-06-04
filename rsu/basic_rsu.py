# /*
# * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# *
# * Licensed under the Apache License, Version 2.0 (the "License").
# * You may not use this file except in compliance with the License.
# * A copy of the License is located at
# *
# *  http://aws.amazon.com/apache2.0
# *
# * or in the "license" file accompanying this file. This file is distributed
# * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# * express or implied. See the License for the specific language governing
# * permissions and limitations under the License.
# */

import os
import sys
import time
import uuid
import json
import logging
import argparse
from AWSIoTPythonSDK.core.greengrass.discovery.providers import DiscoveryInfoProvider
from AWSIoTPythonSDK.core.protocol.connection.cores import ProgressiveBackOffCore
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.exception.AWSIoTExceptions import DiscoveryInvalidRequestException

AllowedActions = ['both', 'publish', 'subscribe']

MAX_DISCOVERY_RETRIES = 10
GROUP_CA_PATH = "./groupCA/"

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--thing", action="store", required=True, dest="thingName")
args = parser.parse_args()

host = 'a2twdhxfhzmdtl-ats.iot.ap-northeast-2.amazonaws.com'
rootCAPath = 'root-ca-cert.pem'
certificatePath = 'cert.pem'
privateKeyPath = 'private.key'
clientId = 'RSU' + str(args.thingName)
thingName = 'RSU' + str(args.thingName)
topic = 'hello/world/pubsub'
mode = 'publish'

publish_topic = []
publish_msg = []

cloud_upload_url = 'http://3.35.184.173:8000/upload/'

# 알고리즘 도로 정보 초기화
from .pathfinding import call_astar as astar
global nodes
nodes = astar.call_astar()
# from pathfinding import call_dijkstra

import rsu_db 

# General message notification callback
def customOnMessage(message):
    global publish_topic
    global publish_msg
    print('Received message on topic %s: %s\n' % (message.topic, message.payload))
    subscribe_topic = message.topic
    payload = json.loads(message.payload)

    topic_split = subscribe_topic.split('/')
    rsu = topic_split[0]
    print('RSU #', rsu)

    if(len(topic_split) == 4) : # trigger - 자신한테 일어나는 경우
        if(topic_split[2] == 'rsu') : # /trigger/rsu/anomaly
            start_rsu = payload['start_rsu']
            end_rsu = payload['end_rsu']
            accident_type = payload['accident_type']
            accident_size = payload['accident_size']
            image_name = payload['image_name']
            basic_image_path = './blurring/' + str(accident_type) + '/'

            # 1. detect license plate
            # loactions = detect(image_name)
            locations = []

            # 2. detect face and blurring
            from .blurring import blurring
            blurred_image_name = blurring.blurring(image_name, locations)

            # 3. send image to cloud
            from .send_image import sendImage
            cloud_image_name = sendImage(basic_image_path + blurred_image_name) # parameter : image name
            print('cloud_image_name : ', cloud_image_name)

            # 4. insert into RSUState
            result = rsu_db.insert_anomaly(rsu, start_rsu, end_rsu, accident_type, accident_size)
            print('insert_anomaly result : ', result)

            # 5. change links weight
            traffic = 10
            astar.change_branch(nodes[start_rsu - 1], nodes[end_rsu - 1], traffic)

            # 6. send anomaly info to near rsu - mqtt publish(n/rsu/anomaly)
            near_rsu = rsu_db.select_near_rsu(rsu) # select near rsu
            for i in near_rsu :
                publish_topic.append(str(i) + '/rsu/anomaly')
                message = {}
                message['start_rsu'] = start_rsu
                message['end_rsu'] = end_rsu
                message['accident_type'] = accident_type
                message['accident_size'] = accident_size
                messageJson = json.dumps(message)
                publish_msg.append(messageJson)
            
            # 7. send anomaly image url to registered obu - mqtt publish(obu/anomaly)
            select_obu = rsu_db.select_near_obu(rsu)
            tmp = 'obu/anomaly'
            publish_topic.append(tmp)
            message = {}
            message['url'] = cloud_upload_url + cloud_image_name
            messageJson = json.dumps(message)
            publish_msg.append(messageJson)

        elif(topic_split[2] == 'obu') : # /trigger/obu/register
            select_obu = rsu_db.select_near_obu(rsu)
            if(len(select_obu) > 0) : # obu가 이미 등록되어있음
                path_db = select_obu[0][1]
                path = path_db.split(',')
            else : # 처음 등록
                # 1. calculate path
                start = int(rsu) 
                destination = int(payload['destination'])
                path = astar.find_path(nodes[start - 1], nodes[destination - 1])
                print(f'{start} -> {destination} : {path}')
                path = list(map(str, path))
                path_db = ','.join(path)
                # 2. insert into OBU(obu id & path)
                result = rsu_db.register_obu(rsu, payload['obu_id'], path)
                print('register_obu result : ', result)
            
            now_idx = path.index(str(rsu))
            if(now_idx >= len(path) - 2) :
                start = end = path[now_idx]
            else :
                start, end = path[now_idx + 1], path[now_idx + 2]

            # 3. send obu info to next rsu - mqtt publish (rsun/obu/register)
            tmp = start + '/obu/register'
            publish_topic.append(tmp)
            message = {}
            message['obu_id'] = payload['obu_id']
            message['path'] = path_db
            messageJson = json.dumps(message)
            publish_msg.append(messageJson)

            # 4. send path to obu - mqtt publish (obu/register)
            publish_topic.append('obu/register')
            message = {}
            message['start'] = start 
            message['end'] = end
            messageJson = json.dumps(message)
            publish_msg.append(messageJson)

            # 5. delete obu info
            result = rsu_db.delete_obu(rsu, payload['obu_id'])


    elif(len(topic_split) == 3) : # 주변 RSU로 부터 전달받는 경우
        if(topic_split[1] == 'rsu' and topic_split[2] == 'anomaly') : # /rsu/anomaly
            start_rsu = payload['start_rsu']
            end_rsu = payload['end_rsu']
            accident_type = payload['accident_type']
            accident_size = payload['accident_size']

            # 1. insert into RSUState
            result = rsu_db.insert_anomaly(rsu, start_rsu, end_rsu, accident_type, accident_size)
            print('insert_anomaly result : ', result)
            # 2. change links weight
            traffic = 10
            astar.change_branch(nodes[start_rsu - 1], nodes[end_rsu - 1], traffic)
        
        elif(topic_split[1] == 'rsu' and topic_split[2] == 'traffic') : # /rsu/traffic
            start_rsu = payload['start_rsu']
            end_rsu = payload['end_rsu']
            accident_type = payload['traffic']

            # change links weight
            traffic = 10
            astar.change_branch(nodes[start_rsu - 1], nodes[end_rsu - 1], int(traffic))

        elif(topic_split[1] == 'obu') : # /obu/register
            path = payload['path']
            print('path : ', path)
            # 1. check anormaly table - if anormaly in path, recalculate path
            result = rsu_db.check_anomaly(rsu, path)
            print('check_anomaly result : ', result)
            if(result) : # path에 이상현상이 있으면 재탐색
                path_result = astar.find_path(nodes[rsu - 1], nodes[path[-1] - 1]) # path를 어떻게 넘겨주는지 확인필요
                print(path_result)
            # 2. insert into OBU
            result = rsu_db.register_obu(rsu, payload['obu_id'], path)
            print('register_obu result : ', result)
            # 3. send obu info to next rsu - mqtt publish (obu/register)
            path_list = path.split(',')
            now_idx = path_list.index(str(rsu))
            if(now_idx == len(path_list) - 1) :
                start = end = path_list[now_idx]
            elif(now_idx == len(path_list) - 2) :
                start = end = path_list[now_idx]
            else :
                start, end = path_list[now_idx + 1], path_list[now_idx + 2]

            tmp = start + '/obu/register'
            publish_topic.append(tmp)
            message = {}
            message['obu_id'] = payload['obu_id']
            message['start'] = start
            message['end'] = end
            messageJson = json.dumps(message)
            publish_msg.append(messageJson)

            publish_topic.append('obu/register')
            message = {}
            message['start'] = start 
            message['end'] = end
            messageJson = json.dumps(message)
            publish_msg.append(messageJson)

            # 5. delete obu info
            result = rsu_db.delete_obu(rsu, payload['obu_id'])

    else : # test
        result = rsu_db.db_test(rsu)
        if(result) :
            print('result : ', result)
            print('Test ok')
        else :
            print('Test failed')

if mode not in AllowedActions:
    # parser.error("Unknown --mode option %s. Must be one of %s" % (mode, str(AllowedActions)))
    print("Unknown --mode option %s. Must be one of %s" % (mode, str(AllowedActions)))
    exit(2)

if not certificatePath or not privateKeyPath:
    # parser.error("Missing credentials for authentication, you must specify --cert and --key args.")
    print("Missing credentials for authentication, you must specify --cert and --key args.")
    exit(2)

if not os.path.isfile(rootCAPath):
    # parser.error("Root CA path does not exist {}".format(rootCAPath))
    print("Root CA path does not exist {}".format(rootCAPath))
    exit(3)

if not os.path.isfile(certificatePath):
    # parser.error("No certificate found at {}".format(certificatePath))
    print("No certificate found at {}".format(certificatePath))
    exit(3)

if not os.path.isfile(privateKeyPath):
    # parser.error("No private key found at {}".format(privateKeyPath))
    print("No private key found at {}".format(privateKeyPath))
    exit(3)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Progressive back off core
backOffCore = ProgressiveBackOffCore()

# Discover GGCs
discoveryInfoProvider = DiscoveryInfoProvider()
discoveryInfoProvider.configureEndpoint(host)
discoveryInfoProvider.configureCredentials(rootCAPath, certificatePath, privateKeyPath)
discoveryInfoProvider.configureTimeout(10)  # 10 sec

retryCount = MAX_DISCOVERY_RETRIES
discovered = False
groupCA = None
coreInfo = None
while retryCount != 0:
    try:
        discoveryInfo = discoveryInfoProvider.discover(thingName)
        caList = discoveryInfo.getAllCas()
        coreList = discoveryInfo.getAllCores()

        # We only pick the first ca and core info
        groupId, ca = caList[0]
        coreInfo = coreList[0]
        print("Discovered GGC: %s from Group: %s" % (coreInfo.coreThingArn, groupId))

        print("Now we persist the connectivity/identity information...")
        groupCA = GROUP_CA_PATH + groupId + "_CA_" + str(uuid.uuid4()) + ".crt"
        if not os.path.exists(GROUP_CA_PATH):
            os.makedirs(GROUP_CA_PATH)
        groupCAFile = open(groupCA, "w")
        groupCAFile.write(ca)
        groupCAFile.close()

        discovered = True
        print("Now proceed to the connecting flow...")
        break
    except DiscoveryInvalidRequestException as e:
        print("Invalid discovery request detected!")
        print("Type: %s" % str(type(e)))
        # print("Error message: %s" % e.message)
        print("Stopping...")
        break
    except BaseException as e:
        # print("Error in discovery!")
        # print("Type: %s" % str(type(e)))
        # print("Error message: %s" % e.message)
        retryCount -= 1
        print("\n%d/%d retries left\n" % (retryCount, MAX_DISCOVERY_RETRIES))
        print("Backing off...\n")
        backOffCore.backOff()

if not discovered:
    print("Discovery failed after %d retries. Exiting...\n" % (MAX_DISCOVERY_RETRIES))
    sys.exit(-1)

# Iterate through all connection options for the core and use the first successful one
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureCredentials(groupCA, privateKeyPath, certificatePath)
myAWSIoTMQTTClient.onMessage = customOnMessage

connected = False
for connectivityInfo in coreInfo.connectivityInfoList:
    currentHost = connectivityInfo.host
    currentPort = connectivityInfo.port
    # print("Trying to connect to core at %s:%d" % (currentHost, currentPort))
    myAWSIoTMQTTClient.configureEndpoint(currentHost, currentPort)
    try:
        myAWSIoTMQTTClient.connect()
        connected = True
        break
    except BaseException as e:
        print("Error in connect!")
        print("Type: %s" % str(type(e)))
        # print("Error message: %s" % e.message)

if not connected:
    # print("Cannot connect to core %s. Exiting..." % coreInfo.coreThingArn)
    sys.exit(-2)

# Successfully connected to the core
if mode == 'both' or mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 0, None)
time.sleep(2)

loopCount = 0
while True:
    try :
        if mode == 'both' or mode == 'publish':
            n = len(publish_topic)
            for i in range(n) :
                time.sleep(3)
                myAWSIoTMQTTClient.publish(publish_topic[i], publish_msg[i], 0)
                print('Published topic %s: %s\n' % (publish_topic[i], publish_msg[i]))
            # if args.mode == 'publish':
            #     print('Published topic %s: %s\n' % (topic, messageJson))
            loopCount += 1
        publish_topic = []
        publish_msg = []
        time.sleep(1)
    except Exception as e :
        print('test_cloud error : ', str(e))
        break
