# -*- coding: utf-8 -*-
import sqlite3
db_name = 'obu.sqlite3'

def create_db() :
    try :
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS RSU (link_id INTEGER PRIMARY KEY AUTOINCREMENT, start INTEGER, end INTEGER, start_latitude TEXT, start_longitude TEXT, end_latitude TEXT, end_longitude TEXT)")
        print('create_db success')
    except Exception as e :
        print(e)
        print('create_db failed')
    finally :
        con.close()

def select_start(obu_loc):
    try:
        obu_loc = obu_loc.split(',')
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("SELECT start from RSU where start_latitude>=%s and start_longitude>=%s and  end_latitude<=%s and end_longitude<=%s" %(obu_loc[0], obu_loc[1], obu_loc[0], obu_loc[1]))
        return str(cur.fetchall())
    except Exception as e:
        print(e)
        print('select_start failed')
    finally:
        con.close

def select_select_rsu_loc(rsu_id):
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("SELECT start_latitude, start_longitude from RSU where start=%d" %(rsu_id))
        return cur.fetchall()[0]
    except Exception as e:
        print(e)
        print('select_start failed')
    finally:
        con.close