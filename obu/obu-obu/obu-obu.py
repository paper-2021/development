import os
import sys
import time

import cv2
import numpy as np
import time
import obu.db_obu as db_obu
from obu.display import htmltopng as htmltopng
from obu.display import modify_js as modify_js

# original rsu part
from rsu.pathfinding import call_astar as astar
global nodes
nodes = astar.call_astar()
import rsu.rsu_db as rsu_db

start = 0 # CHECK
destination = 0 # CHECK
obu_loc = 0
rsu_loc = 0
rsu_id = ''
next_rsu_id = 0
end_next_rsu_id = 0
start_time = 0
time_obu = 0

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
            print("FIND ROUTE=========================")
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

        # 이상현상 감지하기 # TODO -> mqtt 추가하는 지 물어보기
        # mqtt 추가
        state = 'anomaly'
        image = ''

        # 이상현상 감지 시 차 번호 인식 및 블러링
        if(state == 'anomaly'):
            start_rsu = payload['start_rsu']
            end_rsu = payload['end_rsu']
            accident_type = payload['accident_type']
            accident_size = payload['accident_size']
            image_name = payload['image_name']
            send_true = payload['send']
            basic_image_path = './blurring/' + str(accident_type) + '/'
            print(f'start_rsu : {start_rsu}, end_rsu : {end_rsu}, accident_type : {accident_type}, accident_size : {accident_size}, image_name : {image_name}')

            # 1. detect license plate
            # from blurring import detect
            # locations = detect.detect_ip('./' + str(accident_type) + '/' + image_name)
            # locations = locations[1:]
            # print('locations : ', locations)
            if(send_true == '1') :
                locations = [[(686, 416, 802, 468)], [(967, 673, 1073, 705)], [(118.0, 258.0, 201.0, 290.0)]]
                loc = int(payload['loc'])
                
                # 2. detect face and blurring
                from blurring import blurring
                blurred_image_name = blurring.blurring('/home/pi/rsu' + str(real_thing) + '/blurring/' + str(accident_type) + '/' + image_name, locations[loc])

                # 3. send image to cloud
                from send_image import sendImage
                cloud_image_name = sendImage('/home/pi/rsu' + str(real_thing) + '/blurring/' + str(accident_type) + '/' + blurred_image_name) # parameter : image name
                print('cloud_image_name : ', cloud_image_name)
                if(cloud_image_name == False) :
                    cloud_image_name = str(accident_type) + '/' + blurred_image_name

            # 4. insert into RSUState
            result = rsu_db.insert_anomaly(str(rsu), start_rsu, end_rsu, accident_type, accident_size)
            print('insert_anomaly result : ', result)

            # 5. change links weight
            traffic = 10
            # astar.change_branch(nodes[start_rsu - 1], nodes[end_rsu - 1], traffic)
            dij.change_branch(d_nodes[start_rsu - 1], d_nodes[end_rsu - 1], traffic)

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
            
            if(send_true == '1') :
                url = cloud_upload_url + cloud_image_name
            else :
                url = '0'
            # 7. send anomaly image url to registered obu - mqtt publish(obu/anomaly)
            select_obu = rsu_db.select_near_obu(rsu)
            tmp = 'obu/anomaly'
            publish_topic.append(tmp)
            message = {}
            message['start'] = start_rsu
            message['end'] = end_rsu
            message['url'] = url
            messageJson = json.dumps(message)
            publish_msg.append(messageJson)


main()