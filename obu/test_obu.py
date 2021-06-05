# -*- coding: utf-8 -*-
# worken cv -> source ~/.profile
# python 3 ---
# 37.508379, 127.037166
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

import cv2
import numpy as np
import time
import db_obu
from display import htmltopng as htmltopng
from display import modify_js as modify_js

AllowedActions = ['both', 'publish', 'subscribe']

MAX_DISCOVERY_RETRIES = 10
GROUP_CA_PATH = "./groupCA/"

parser = argparse.ArgumentParser()
#parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
#parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
#parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
#parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
#parser.add_argument("-n", "--thingName", action="store", dest="thingName", default="Bot", help="Targeted thing name")
#parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
#parser.add_argument("-m", "--mode", action="store", dest="mode", default="both", help="Operation modes: %s"%str(AllowedActions))
#parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!", help="Message to publish")

args = parser.parse_args()
host = 'a2twdhxfhzmdtl-ats.iot.ap-northeast-2.amazonaws.com' #args.host
rootCAPath = 'root-ca-cert.pem' #args.rootCAPath
certificatePath = '8dc995a116.cert.pem' #args.certificatePath
privateKeyPath = '8dc995a116.private.key' #args.privateKeyPath
clientId = 'OBU' #args.thingName
thingName = 'OBU' #args.thingName
topic = 'obu/#' #args.topic
args.mode = 'publish'
args.message = 'Start'
obu_id = 1
destination = '78'
obu_loc = '37.508, 127.037' # NOTE start obu 위치 여기 넣기
publish_topic = []
publish_msg = []
rsu_id = ''
next_rsu_id = ''
end_next_rsu_id = ''
route = ""
start_time = 0
time_obu = 0

#http://3.35.184.173:8000/upload/3/20210507212215_3_accident.jpg -> image

def find_obu():
    global start_time
    global time_obu
    if rsu_id == '':
        return obu_loc
    if(time.time() - start_time >= time_obu):
        time_obu = db_obu.select_dis(rsu_id, next_rsu_id) *10
        print("=====find_obu==========%f============" %(time_obu))
        start_time = time.time()
        rsu_loc = db_obu.select_rsu_loc(rsu_id)
        return rsu_loc[0]+' ,'+rsu_loc[1]

def customOnMessage(message):
    global rsu_id
    global next_rsu_id
    global end_next_rsu_id
    global obu_loc
    global destination
    subscribe_topic = message.topic
    payload = json.loads(message.payload)
    print("=======IN============================"+str(message.payload))
    situation = False # anomaly, True
    if(subscribe_topic == 'obu/start'):
        print('=============obu/start=============')
        # 1. regiter rsu
        message = {}
        rsu_id = ''
        modify_js.init_map()
        message['obu_id'] = obu_id
        # 1-1 obu location에서 담당하는 rsu_id 찾기
        obu_loc = find_obu() #ex: '37.518, 127.050'
        rsu_id = db_obu.select_start(obu_loc) #ex: 9
        message['destination'] = destination # input 목적지 node 
        # 1-2 send mqtt
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(str(rsu_id) + '/trigger/obu/register', messageJson, 0)
        print("===========Send message"+ str(message)+"  topic: "+ str(rsu_id) + '/trigger/obu/register===========')
    elif(subscribe_topic == 'obu/register'):
        print('=============obu/register=============')
        # 2. show alarm
        # 2.-1 현재 rsu와 다음 rsu 위치 구하기
        next_rsu_id = payload['start'] #(9)ex: '37.518, 127.050'
        end_next_rsu_id = payload['end'] 
        if(next_rsu_id == end_next_rsu_id and destination == next_rsu_id):
            print("============= Arrive =============")
            exit()
        time_obu = db_obu.select_dis(rsu_id, next_rsu_id) 
        obu_loc = find_obu() #ex: '37.518, 127.050', # 현재 OBU 위치 받기
        rsu_loc = db_obu.select_rsu_loc(rsu_id) #(10)ex: '37.513, 127.053'
        next_rsu_loc = db_obu.select_rsu_loc(next_rsu_id)
        end_next_rsu_loc = db_obu.select_rsu_loc(end_next_rsu_id)
        rsu_loc = rsu_loc[0]+', ' + rsu_loc[1]
        next_rsu_loc = next_rsu_loc[0]+ ', '+next_rsu_loc[1]
        end_next_rsu_loc = end_next_rsu_loc[0]+ ', '+end_next_rsu_loc[1]
        data_next = [str(obu_loc), str(rsu_loc), str(next_rsu_loc), str(end_next_rsu_loc)] 
        # 2-2 modify js
        html_file = modify_js.modify_html(False, data_next)
        with open('display/html/index.html', 'w') as file:
            file.write(html_file)
        # 2-3 제작한 화면 png로 바꾸기
        #htmltopng.change_htmltopng('index.html') 
        # 2-4 화면 띄우기
        #import cv2
        #image = cv2.imread('display/image/map.png', cv2.IMREAD_COLOR)
        #cv2.imshow("map", image) # 윈도우 창에 이미지를 띄운다.
        #cv2.waitKey(0) # time 마다 키 입력사애를 받아온다. 0일 경우 키 입력이 될 때 까지 기다린다.
        #cv2.destroyAllWindows() # 모든 윈도우창을 닫는다.
    elif(subscribe_topic == 'obu/anomaly'): # TEST
        print('=============obu/anomaly=============')
        # 2. show alarm
        # 2.-1 현재 rsu와 다음 rsu 위치 구하기
        next_rsu_id = payload['start'] #(9)ex: '37.518, 127.050'
        end_next_rsu_id = payload['end'] 
        obu_loc = find_obu() #ex: '37.518, 127.050', # 현재 OBU 위치 받기
        rsu_loc = db_obu.select_rsu_loc(rsu_id) #(10)ex: '37.513, 127.053'
        next_rsu_loc = db_obu.select_rsu_loc(next_rsu_id)
        end_next_rsu_loc = db_obu.select_rsu_loc(end_next_rsu_id)
        rsu_loc = rsu_loc[0]+', ' + rsu_loc[1]
        next_rsu_loc = next_rsu_loc[0]+ ', '+next_rsu_loc[1]
        end_next_rsu_loc = end_next_rsu_loc[0]+ ', '+end_next_rsu_loc[1]
        data_next = [str(obu_loc), str(rsu_loc), str(next_rsu_loc), str(end_next_rsu_loc)] 
        #data_next.append('http://3.35.184.173:8000/upload/3/20210507212215_3_accident.jpg')
        data_next.append(payload['url'])
        # 2-2 modify js
        html_file = modify_js.modify_html(True, data_next)
        with open('index.html', 'w') as file:
            file.write(html_file)
        # 2-3 제작한 화면 png로 바꾸기
        #htmltopng.change_htmltopng('index.htmll')
        # 2-4 화면 띄우기
        #image = cv2.imread('display/image/map.png', cv2.IMREAD_COLOR)
        #cv2.imshow("map", image) # 윈도우 창에 이미지를 띄운다.
        #cv2.waitKey(0) # time 마다 키 입력사애를 받아온다. 0일 경우 키 입력이 될 때 까지 기다린다.
        #cv2.destroyAllWindows() # 모든 윈도우창을 닫는다.


if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if not certificatePath or not privateKeyPath:
    parser.error("Missing credentials for authentication, you must specify --cert and --key args.")
    exit(2)

if not os.path.isfile(rootCAPath):
    parser.error("Root CA path does not exist {}".format(rootCAPath))
    exit(3)

if not os.path.isfile(certificatePath):
    parser.error("No certificate found at {}".format(certificatePath))
    exit(3)

if not os.path.isfile(privateKeyPath):
    parser.error("No private key found at {}".format(privateKeyPath))
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
        print(e)
        print("Stopping...")
        break
    except BaseException as e:
        print("Error in discovery!")
        print("Type: %s" % str(type(e)))
        print(e)
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
    print("Trying to connect to core at %s:%d" % (currentHost, currentPort))
    myAWSIoTMQTTClient.configureEndpoint(currentHost, currentPort)
    try:
        myAWSIoTMQTTClient.connect()
        connected = True
        break
    except BaseException as e:
        print("Error in connect!")
        print("Type: %s" % str(type(e)))
        print(e)

if not connected:
    print("Cannot connect to core %s. Exiting..." % coreInfo.coreThingArn)
    sys.exit(-2)

# Successfully connected to the core
if args.mode == 'both' or args.mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 0, None)
time.sleep(2)

loopCount = 0
while True:
    print("========================")
    myAWSIoTMQTTClient.publish('trigger/start', 'Start', 0)
    try:
        print("=============== Route: %s -> %s" %(rsu_id, next_rsu_id))
        # find next rsu
        print(time_obu, start_time)
        if(time_obu != 0 and time.time() - start_time >= time_obu):
            print("======= Start content next RSU %s" %(next_rsu_id))
            # make message
            message = {}
            rsu_id = next_rsu_id
            start_time = time.time()
            message['obu_id'] = obu_id
            # send mqtt
            messageJson = json.dumps(message)
            myAWSIoTMQTTClient.publish(str(rsu_id) + '/trigger/obu/register', messageJson, 0)
            print("===========Send message"+ str(message)+"  topic: "+ str(rsu_id) + '/trigger/obu/register===========')
    except Exception as e:
        print(e)
        print('OBU Error')
    time.sleep(3)