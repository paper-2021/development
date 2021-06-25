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

import cv2
import numpy as np
import time

# original obu part
import obu.db_obu as db_obu
from obu.display import htmltopng as htmltopng
from obu.display import modify_js as modify_js

# original rsu part
from rsu.pathfinding import call_astar as astar
global nodes
nodes = astar.call_astar()
import obu.obu-obu.db_OBUver3 as rsu_db

# Greengrass Iot device part
AllowedActions = ['both', 'publish', 'subscribe']
MAX_DISCOVERY_RETRIES = 10
GROUP_CA_PATH = "./groupCA/"
parser = argparse.ArgumentParser()
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

def customOnMessage(message):
    global state
    subscribe_topic = message.topic
    payload = json.loads(message.payload)
    print(f'Received mqtt: ========================= {message.payload} {message.topic}')
    #이상현상 감시지
    if(message.topic == 'obu/trigger/anomaly'):
        state = ('anomaly', payload)


start = 0 # CHECK
destination = 0 # CHECK
obu_loc = 0
rsu_loc = 0
rsu_id = ''
next_rsu_id = 0
end_next_rsu_id = 0
start_time = 0
time_obu = 0
state = ''
cloud_upload_url = 'http://13.125.11.117:8000/upload/'

def find_obu():
    global start_time
    global time_obu
    if rsu_id == '':
        return obu_loc
    if(time.time() - start_time >= time_obu):
        time_obu = db_obu.select_dis(rsu_id, next_rsu_id)*15
        start_time = time.time()
        return rsu_loc

def main():
    global start
    global destination
    global rsu_id
    global next_rsu_id
    global end_next_rsu_id
    global time_obu
    global state
    state = 'start'
    while(True):
        if(state == 'start'):
            #1.start find route
            print("OBU/START =========================")

            #2. input start, destination
            start= 0
            destination = 0
            rsu_id = start
            modify_js.init_map()
            modify_js.set_loc(db_obu.select_rsu_loc(start), db_obu.select_rsu_loc(destination)) #set start, end
            state = 'find_route'

            #3. find route
            print("FIND ROUTE =========================")
            path = astar.find_path(nodes[start - 1], nodes[destination - 1])
            print(f'{start} -> {destination} : {path}')
            path = list(map(str, path))
            path_db = ','.join(path)
            result = rsu_db.register_obu(rsu_id, start, path)
            print('register_obu result : ', result)

            #4.decide rsu and next rsu
            now_idx = path.index(str(start))
            if(now_idx == len(path) - 2) :
                rsu_id = next_rsu_id = path[now_idx + 1]
            elif(now_idx == len(path) - 1) :
                rsu_id = next_rsu_id = path[now_idx]
            else :
                rsu_id, next_rsu_id = path[now_idx + 1], path[now_idx + 2]
            time_obu = db_obu.select_dis(rsu_id, next_rsu_id) 
            rsu_loc = db_obu.select_rsu_loc(rsu_id) #(10)ex: '37.513, 127.053'
            next_rsu_loc = db_obu.select_rsu_loc(next_rsu_id)
            end_next_rsu_loc = db_obu.select_rsu_loc(end_next_rsu_id)
            rsu_loc = rsu_loc[0]+', ' + rsu_loc[1]
            obu_loc = find_obu()
            next_rsu_loc = next_rsu_loc[0]+ ', '+next_rsu_loc[1]
            end_next_rsu_loc = end_next_rsu_loc[0]+ ', '+end_next_rsu_loc[1]
            data_next = [str(rsu_loc), str(rsu_loc), str(next_rsu_loc), str(end_next_rsu_loc)] 
            obu_loc = rsu_loc

            #5. modify js
            html_file = modify_js.modify_html(False, data_next)
            with open('obu/display/html/index.html', 'w') as file:
                file.write(html_file)
            
            #6. delete obu info
            result = rsu_db.delete_obu(start, 1)
            print('delete obu result : ', result)

        # 다음 경로 받는 함수(경우에 따라)
        if(time_obu != 0 and time.time() - start_time >= time_obu):
            #1. find obu info
            select_obu = rsu_db.select_near_obu(rsu_id)
            path_db = select_obu[0][1]
            path = path_db.split(',')

            #2..decide rsu and next rsu
            now_idx = path.index(str(start))
            if(now_idx == len(path) - 2) :
                rsu_id = next_rsu_id = path[now_idx + 1]
            elif(now_idx == len(path) - 1) :
                rsu_id = next_rsu_id = path[now_idx]
            else :
                rsu_id, next_rsu_id = path[now_idx + 1], path[now_idx + 2]
            time_obu = db_obu.select_dis(rsu_id, next_rsu_id) 
            rsu_loc = db_obu.select_rsu_loc(rsu_id) #(10)ex: '37.513, 127.053'
            next_rsu_loc = db_obu.select_rsu_loc(next_rsu_id)
            end_next_rsu_loc = db_obu.select_rsu_loc(end_next_rsu_id)
            rsu_loc = rsu_loc[0]+', ' + rsu_loc[1]
            obu_loc = find_obu()
            next_rsu_loc = next_rsu_loc[0]+ ', '+next_rsu_loc[1]
            end_next_rsu_loc = end_next_rsu_loc[0]+ ', '+end_next_rsu_loc[1]
            data_next = [str(rsu_loc), str(rsu_loc), str(next_rsu_loc), str(end_next_rsu_loc)] 
            obu_loc = rsu_loc

            #3. modify js
            html_file = modify_js.modify_html(False, data_next)
            with open('obu/display/html/index.html', 'w') as file:
                file.write(html_file)
            
            #4. delete obu info
            result = rsu_db.delete_obu(start, 1)
            print('delete obu result : ', result)

        # 이상현상 감지 시 차 번호 인식 및 블러링
        if(state[1] == 'anomaly'):
            print('START ANOMALY PART =========================')
            payload = state[1]
            start_rsu = payload['start_rsu']
            end_rsu = payload['end_rsu']
            accident_type = payload['accident_type']
            accident_size = payload['accident_size']
            image_name = payload['image_name']
            send_true = payload['send']
            basic_image_path = './blurring/' + str(accident_type) + '/'
            print(f'start_rsu : {start_rsu}, end_rsu : {end_rsu}, accident_type : {accident_type}, accident_size : {accident_size}, image_name : {image_name}')

            # 1. detect license plate
            if(send_true == '1') :
                locations = [[(686, 416, 802, 468)], [(967, 673, 1073, 705)], [(118.0, 258.0, 201.0, 290.0)]]
                loc = int(payload['loc'])
                
                # 2. detect face and blurring
                from rsu.blurring import blurring
                blurred_image_name = blurring.blurring('/home/pi/obu' + '/blurring/' + str(accident_type) + '/' + image_name, locations[loc])

                # 3. send image to cloud
                from rsu.send_image import sendImage
                cloud_image_name = sendImage('/home/pi/obu' + '/blurring/' + str(accident_type) + '/' + blurred_image_name) # parameter : image name
                print('cloud_image_name : ', cloud_image_name)
                if(cloud_image_name == False) :
                    cloud_image_name = str(accident_type) + '/' + blurred_image_name

            # 4. insert into RSUState
            result = rsu_db.insert_anomaly(str(rsu_id), start_rsu, end_rsu, accident_type, accident_size)
            print('insert_anomaly result : ', result)

            # 5. change links weight
            traffic = 10
            astar.change_branch(nodes[start_rsu - 1], nodes[end_rsu - 1], traffic)
            
            # 6. send anomaly info to near rsu - mqtt publish(n/rsu/anomaly) #TODO
            near_rsu = rsu_db.select_near_rsu(rsu) # select near rsu
            for i in near_rsu :
                rsu_db.insert_anomaly(str(i), start_rsu, end_rsu, accident_type, accident_size)
            
            if(send_true == '1') :
                url = cloud_upload_url + cloud_image_name
            else :
                url = '0'

            # 7. show anomaly alarm

            # 2.-1 현재 rsu와 다음 rsu 위치 구하기
            rsu_list = [str(rsu_id), str(next_rsu_id), str(end_next_rsu_id)]
            start = start_rsu
            end = end_rsu
            #print("=============rsu_list: %s ====== anomaly list: %s, %s" %(str(rsu_list), start, end))
            if(start in rsu_list or end in rsu_list):
                link_loc = db_obu.find_link(start_rsu, end_rsu)
                link_loc = str(link_loc[0])+', ' + str(link_loc[1])
                start_loc = db_obu.select_rsu_loc(start)
                end_loc = db_obu.select_rsu_loc(end)
                start_loc = start_loc[0]+', ' + start_loc[1]
                end_loc = end_loc[0]+', ' + end_loc[1]
                data_next = [str(obu_loc), str(link_loc), str(0)] 
                data_next.append(url)
                data_next += [start_loc, end_loc]
                # 2-2 modify js
                html_file = modify_js.modify_html(True, data_next)
                with open('obu/display/html/index.html', 'w') as file:
                    file.write(html_file)

main()