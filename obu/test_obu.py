# -*- coding: utf-8 -*-
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

import pdfcrowd
import cv2
import numpy as np

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
rootCAPath = 'root-ca-cer.pem' #args.rootCAPath
certificatePath = '8dc995a116.cert.pem' #args.certificatePath
privateKeyPath = '8dc995a116.private.key' #args.privateKeyPath
clientId = 'OBU' #args.thingName
thingName = 'OBU' #args.thingName
topic = 'hello/world/pubsub' #args.topic
args.mode = 'publish'
args.message = 'Start'
obu_id = '1'
publish_topic = []
publish_msg = []
rsu_id = ''
route = ""

#http://3.35.184.173:8000/upload/3/20210507212215_3_accident.jpg -> image

def modify_js(situation, data):
    """
    data
    situation : false -> [obu_loc, start_loc, end_loc]
    situation : true  -> [obu_loc, start_loc, end_loc, imagename]
    """
    js_file = ''
    global route
    route += """new Tmapv2.LatLng("""+data[1]+ """),
            new Tmapv2.LatLng(""" + data[2] + """),"""
    if(situation):
        js_file = """
var map, marker;
function initTmap(){
    var map = new Tmapv2.Map("map_div",  
    {
        center: new Tmapv2.LatLng(37.495, 127.021),
        width: "1500px", 
        height: "700px",
        zoom: 14
    });
    var rsu = new Tmapv2.Marker({
        position: new Tmapv2.LatLng(""" + data[2]+ """),
        map: map
    });
    var polyline = new Tmapv2.Polyline({
        path: [ """ + route + """],
        strokeColor: "#dd00dd",
		strokeWeight: 6, 
		draggable: true, 
		strokeStyle:'dot',
		outline: true, 
		outlineColor:'#ffffff',
		map: map 
    });
    var car = new Tmapv2.Marker({
        position: new Tmapv2.LatLng("""+data[0]+"""), 
        icon: "images/page_1/car.png", 
        map: map 
    });

    document.getElementById("u4_img").src = """+ data[3]+ """;
} 
        """
    else:
        js_file = """
var map, marker;
function initTmap(){
    var map = new Tmapv2.Map("map_div",  
    {
        center: new Tmapv2.LatLng(37.495, 127.021), 
        width: "1500px", 
        height: "700px",
        zoom: 14
    });
    
    var polyline = new Tmapv2.Polyline({
        path: ["""+ route + """],
        strokeColor: "#dd00dd",
		strokeWeight: 6,
		draggable: true, 
		strokeStyle:'dot', 
		outline: true,
		outlineColor:'#ffffff',
		map: map 
    });

    var car = new Tmapv2.Marker({
        position: new Tmapv2.LatLng("""+data[0]+"""),
        icon: "images/page_1/car.png", 
        map: map 
    });
} 
"""
    return js_file

# html to png
def change_htmltopng (htmlfile):
    try:
        # create the API client instance
        client = pdfcrowd.HtmlToImageClient('demo', 'ce544b6ea52a5621fb9d55f8b542d14d')
        # configure the conversion
        client.setOutputFormat('png')
        # run the conversion and write the result to a file
        client.convertFileToFile('html/'+htmlfile, 'image/map.png')
    except pdfcrowd.Error as why:
        # report the error
        sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))
        # rethrow or handle the exception
        raise

def customOnMessage(message):
    import db_obu
    global publish_topic
    global publish_msg
    global rsu_ip
    #print('Received message on topic %s: %s\n' % (message.topic, message.payload))
    subscribe_topic = message.topic
    payload = json.loads(message.payload)
    situation = False # anomaly, True
    if(subscribe_topic == str(obu_id) + '/trigger/obu/start'):
        print('=============%d/trigger/obu/start============='%(obu_id))
        # 1. regiter rsu
        message = {}
        rsu_id = ''
        route = ""
        message['obu_id'] = obu_id
        # 1-1 obu location에서 담당하는 rsu_id 찾기
        obu_loc = 'obu_location' #ex: '37.518, 127.050'
        rsu_id = db_obu.select_start(obu_loc) #ex: 9
        messsage['obu_location'] = obu_loc
        message['destination'] = ('위도', '경도') # input 목적지, (65)ex: 37.493, 127.013 
        # 1-2 send mqtt
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(str(rsu_id) + '/trigger/obu/register', messageJson, 0)
    elif(subscribe_topic == str(obu_id) + '/obu/register'):
        print('=============%d/obu/register=============' %(obu_id))
        # 2. show alarm
        # 2.-1 현재 rsu와 다음 rsu 위치 구하기
        situation = False
        obu_loc = 'obu_location' #ex: '37.518, 127.050', # 현재 OBU 위치 받기
        next_rsu_id = payload['rsu_id'] #(9)ex: '37.518, 127.050'
        rsu_loc = db_obu.select_rsu_loc(rsu_id) #(10)ex: '37.513, 127.053'
        next_rsu_loc = db_obu.select_rsu_loc(next_rsu_id)
        rsu_loc = str(int(rsu_loc[0]))+', ' + str(int(rsu_loc[1]))
        next_rsu_loc = str(int(next_rsu_loc[0]))+ ', '+str(int(next_rsu_loc[1]))
        data_next = [obu_loc, rsu_loc, next_rsu_loc]
        if(situation):
            data_next.append('http://3.35.184.173:8000/upload/3/20210507212215_3_accident.jpg')
        # 2-2 modify js
        js_file = modify_js(situation, data_next)
        with open('html/map_js.js', 'w') as file:
            file.write(js_file)
        # 2-3 제작한 화면 png로 바꾸기
        if(situation):
            change_htmltopng('map_traffic.html')
        else:
            change_htmltopng('map_normal.html') 
        # 2-4 화면 띄우기
        image = cv2.imread('image/map.png', cv2.IMREAD_COLOR)
        cv2.imshow("map", image) # 윈도우 창에 이미지를 띄운다.
        cv2.waitKey(0) # time 마다 키 입력사애를 받아온다. 0일 경우 키 입력이 될 때 까지 기다린다.
        cv2.destroyAllWindows() # 모든 윈도우창을 닫는다.


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
    print("Trying to connect to core at %s:%d" % (currentHost, currentPort))
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
    print("Cannot connect to core %s. Exiting..." % coreInfo.coreThingArn)
    sys.exit(-2)

# Successfully connected to the core
if args.mode == 'both' or args.mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 0, None)
time.sleep(2)

loopCount = 0
if args.mode == 'both' or args.mode == 'publish':
    message = {}
    message['message'] = args.message
    message['sequence'] = loopCount
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 0)
    if args.mode == 'publish':
        print('Published topic %s: %s\n' % (topic, messageJson))
    loopCount += 1

