# -*- coding: utf-8 -*-
import sqlite3
from haversine import haversine
db_name = 'obu.sqlite3'

def select_start(obu_loc):
    try:
        obu_loc = obu_loc.split(',')
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("SELECT start from RSU where start_latitude>=%s and start_longitude>=%s and  end_latitude<=%s and end_longitude<=%s" %(obu_loc[0], obu_loc[1], obu_loc[0], obu_loc[1]))
        return str(cur.fetchall()[0][0])
    except Exception as e:
        print(e)
        print('select_start failed')
    finally:
        con.close

def select_rsu_loc(rsu_id):
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("SELECT start_latitude, start_longitude from RSU where start=%s" %(rsu_id))
        return cur.fetchall()[0]
    except Exception as e:
        print(e)
        print('select_start failed %s' %(rsu_id))
    finally:
        con.close

def select_dis(start, end):
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("SELECT start_latitude, start_longitude, end_latitude, end_longitude from RSU where start=%s and end= %s" %(start, end))
        data = cur.fetchall()
        if(data == []):
            cur.execute("SELECT start_latitude, start_longitude, end_latitude, end_longitude from RSU where start=%s and end= %s" %(end, start))
            data = cur.fetchall()
        data = [float(i) for i in data[0]]
        return haversine((data[0], data[1]), (data[2],data[3]), unit = 'km')
    except Exception as e:
        print(e)
        print('select distance error %s -> %s' %(start, end))
    finally:
        con.close

def find_link(start, end):
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("SELECT start_latitude, start_longitude, end_latitude, end_longitude from RSU where start=%s and end= %s" %(start, end))
        data = cur.fetchall()
        if(data == []):
            cur.execute("SELECT start_latitude, start_longitude, end_latitude, end_longitude from RSU where start=%s and end= %s" %(end, start))
            data = cur.fetchall()
        data = [float(i) for i in data[0]]
        return ((data[0]+data[2])/2, (data[1]+data[3])/2)
    except Exception as e:
        print(e)
        print('Find link error %s -> %s' %(start, end))
    finally:
        con.close


print(select_rsu_loc('78'))
#print(select_start('37.508, 127.037'))