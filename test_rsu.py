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

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-n", "--thingName", action="store", dest="thingName", default="Bot", help="Targeted thing name")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                    help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                    help="Message to publish")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
clientId = args.thingName
thingName = args.thingName # RSUn
topic = args.topic

rsu_id = int(thingName[3:])
print("================rsu_id(%d)================" %(rsu_id))

publish_topic = []
publish_msg = []

import rsu_db
# General message notification callback
def customOnMessage(message):
    global publish_topic
    global publish_msg
   #  print('Received message on topic %s: %s\n' % (message.topic, message.payload))
    subscribe_topic = message.topic
    payload = json.loads(message.payload)
    if(subscribe_topic == str(rsu_id) + '/trigger/rsu/anomaly') :
        print('=============%d/trigger/rsu/anomaly=============' %(rsu_id))
        # 1. send image to cloud
        from sendImage import sendImage
        sendImage_result = sendImage() # parameter : image name
        print('sendImage_result : ', sendImage_result)
        # 2. insert into RSUState
        result = rsu_db.insert_anomaly(rsu_id, payload['accident_type'], payload['accident_size'])
        print('insert_anomaly result : ', result)
        # 3. send anormaly info to near rsu - mqtt publish(n/rsu/anormaly)
        near_rsu = rsu_db.select_near_rsu() # select near rsu
        for i in near_rsu :
            publish_topic.append(str(i) + '/rsu/anomaly')
            message = {}
            message['rsu_id'] = rsu_id
            message['accident_type'] = payload['accident_type']
            message['accident_size'] = payload['accident_size']
            messageJson = json.dumps(message)
            publish_msg.append(messageJson)
    elif(subscribe_topic == str(rsu_id) + '/trigger/obu/register') :
        print('=============%d/trigger/obu/register=============' %(rsu_id))
        # 1. calculate path
        # start = int(thingName)
        # destination = payload['destination']
        # path = pathfind(start, destination)
        path = '1, 2, 3, 4'
        # 2. insert into OBU(obu id & path)
        result = rsu_db.register_obu(payload['obu_id'], path)
        print('register_obu result : ', result)
        # 3. send obu info to next rsu - mqtt publish (obu/register)
        next_rsu = 2 # find next rsu in path
        tmp = str(next_rsu) + '/obu/register'
        publish_topic.append(tmp)
        message = {}
        message['obu_id'] = payload['obu_id']
        message['path'] = path
        messageJson = json.dumps(message)
        publish_msg.append(messageJson)
    elif(subscribe_topic == str(rsu_id) + '/rsu/anomaly') :
        print('=============%d/rsu/anomaly=============' %(rsu_id))
        # 1. insert into RSUState
        result = rsu_db.insert_anomaly(payload['rsu_id'], payload['accident_type'], payload['accident_size'])
        print('insert_anomaly result : ', result)
    elif(subscribe_topic == str(rsu_id) + '/obu/register') :
        print('=============%d/obu/register=============' %(rsu_id))
        path = payload['path']
        # 1. check anormaly table - if anormaly in path, recalculate path
        result = rsu_db.check_anomaly(path)
        print('check_anomaly result : ', result)
        if(result) :
            # path = pathfind(start, destination)
            path = "1, 3, 4"
        # 2. insert into OBU
        result = rsu_db.register_obu(payload['obu_id'], path)
        print('register_obu result : ', result)
        # 3. send obu info to next rsu - mqtt publish (obu/register)
        next_rsu = 3
        tmp = str(next_rsu) + '/obu/register'
        publish_topic.append(tmp)
        message = {}
        message['obu_id'] = payload['obu_id']
        message['path'] = path
        messageJson = json.dumps(message)
        publish_msg.append(messageJson)

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if not args.certificatePath or not args.privateKeyPath:
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
        print("Error message: %s" % e.message)
        print("Stopping...")
        break
    except BaseException as e:
        print("Error in discovery!")
        print("Type: %s" % str(type(e)))
        print("Error message: %s" % e.message)
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
        print("Error message: %s" % e.message)

if not connected:
    # print("Cannot connect to core %s. Exiting..." % coreInfo.coreThingArn)
    sys.exit(-2)

# Successfully connected to the core
if args.mode == 'both' or args.mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 0, None)
time.sleep(2)

loopCount = 0
while True:
    try :
        global publish_topic
        global publish_msg
        if args.mode == 'both' or args.mode == 'publish':
            n = len(publish_topic)
            for i in range(n) :
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
