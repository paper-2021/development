# -*- coding: utf-8 -*-

# 데이터 베이스를 생성해서 output을 output.txt에 넣는 코드
import sqlite3

conn = sqlite3.connect('check.db')
cur = conn.cursor()

try:
    cur.execute("CREATE TABLE RSU(rsu_id INTEGER PRIMARY KEY, rsu_ip TEXT, location TEXT);")
    cur.close()
    conn.close()
except sqlite3.OperationalError:
    print('table color already exist')

# 데이터 베이스에 집어 넣는 프로그램
def insert_db(table, data):
    cur.execute("INSERT INTO " + table + " VALUES " + data)
    conn.commit()
    cur.close()
    conn.close()
    return "Sucessfully insert the data in " + table

def select_db(rsu_ip):
    cur.execute("SELECT location from RSU where rsu_ip = " + rsu_ip)
    return str(cur.fetchall())