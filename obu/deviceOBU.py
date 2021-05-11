# -*- coding: utf-8 -*-
import pdfcrowd
import sys
import cv2
import numpy as np

import db_obu

# html을 image로 바꾸는 function
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

#situation에 true , false로 이상현상에 벌어졌는지 아닌지 나올 예정
def modify_js(situation, data):
    """
    data
    situation : false -> [start_loc, end_loc]
    situation : true  -> [start_loc, end_loc, imagename]
    """
    js_file = ''
    if(situation):
        js_file = """
var map, marker;

function initTmap(){
    var map = new Tmapv2.Map("map_div",  
    {
        center: new Tmapv2.LatLng(37.261851,127.031121), // 수원시청을 중심으로
        width: "1500px", 
        height: "700px",
        zoom: 16
    });
    // 마커 생성, 마커 이미지 유진이랑 상의하고 바꾸기
    var rsu = new Tmapv2.Marker({
        position: new Tmapv2.LatLng(start_loc_marker), //Marker의 중심좌표 설정, start_loc의 start 위치
        map: map //Marker가 표시될 Map 설정..
    });
    //경로 그려주기, 화살표만들기 가능한지 해보기 45도로
    var polyline = new Tmapv2.Polyline({
        path: [
            new Tmapv2.LatLng(start_loc), // 선의 꼭짓점 좌표
            new Tmapv2.LatLng(end_loc), // 선의 꼭짓점 좌표
        ],
        strokeColor: "#dd00dd", // 라인 색상
		strokeWeight: 6, // 라인 두께
		draggable: true, //드래그 여부
		strokeStyle:'dot', // 선의 종류 soild, dash,
		outline: true, // 외각 선을 설정
		outlineColor:'#ffffff', // 외각 선 색상
		map: map // 지도 객체
    });

    document.getElementById("u4_img").src = abnomality_image;

} 


        """
        js_file.replace('start_loc_marker', data[1])
        js_file.replace('start_loc', data[0])
        js_file.replace('end_loc', data[1])
        js_file.replace('abnomality_image', data[2])

    else:
        js_file = """
var map, marker;

function initTmap(){
    var map = new Tmapv2.Map("map_div",  
    {
        center: new Tmapv2.LatLng(37.261851,127.031121), // 수원시청을 중심으로
        width: "1500px", 
        height: "700px",
        zoom: 16
    });

    //경로 그려주기, 화살표만들기 가능한지 해보기 45도로
    var polyline = new Tmapv2.Polyline({
        path: [
            new Tmapv2.LatLng(start_loc), // 선의 꼭짓점 좌표
            new Tmapv2.LatLng(end_loc), // 선의 꼭짓점 좌표
        ],
        strokeColor: "#dd00dd", // 라인 색상
		strokeWeight: 6, // 라인 두께
		draggable: true, //드래그 여부
		strokeStyle:'dot', // 선의 종류 soild, dash,
		outline: true, // 외각 선을 설정
		outlineColor:'#ffffff', // 외각 선 색상
		map: map // 지도 객체
    });
} 

        """
        js_file.replace('start_loc', data[0])
        js_file.replace('end_loc', data[1])
    
    return js_file

situation = False
# 신호가 들어오면 
rsu_ip = '' # 받은 정보
next_rsu_loc = db_obu.select_db(rsu_ip)
data = next_rsu_loc.split('/')
if(situation):
    pass # data.append(image)로 추가하기 나중에

#js 수정하기
js_file = modify_js(situation,) # 나중에 꼭 수정 -------------------------------------------------
with open('html/map_js.js', 'w') as file:
    file.write(js_file)

if(situation):
    change_htmltopng('map_traffic.html')
else:
    change_htmltopng('map_normal.html') 

# cv2로 안되면 matpotlib로 되는 방법 해보기
image = cv2.imread('image/map.png', cv2.IMREAD_COLOR)
cv2.imshow("map", image) # 윈도우 창에 이미지를 띄운다.
cv2.waitKey(0) # time마다 키 입력사애를 받아온다. 0일 경우 키 입력이 될 때 까지 기다린다.
cv2.destroyAllWindows() # 모든 윈도우창을 닫는다.


