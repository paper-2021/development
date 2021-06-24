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
            select_obu = rsu_db.select_near_obu(rsu_id) # TODO

        # 이상현상 감지하기

        # 이상현상 감지 시 차 번호 인식 및 블러링

main()