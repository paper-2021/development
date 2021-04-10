# 데이터 베이스를 생성해서 output을 output.txt에 넣는 코드
import sqlite3
import sys

sys.stdout = open('output.txt', 'w')

conn = sqlite3.connect('check.db')
cur = conn.cursor()
cur.execute("CREATE TABLE RSU(rsu_id INTEGER PRIMARY KEY, rsu_ip TEXT);")
cur.execute("CREATE TABLE NearRSU(rsu_id INTEGER PRIMARY KEY, FOREIGN KEY(rsu_id) REFERENCES RSU(rsu_id));")
cur.execute("CREATE TABLE RSUState(state_id INTEGER PRIMARY KEY, rsu_id INTEGER, accident_type INTEGER, accident_size INTEGER, traffic INTEGER, FOREIGN KEY(rsu_id) REFERENCES RSU(rsu_id));")
cur.execute("CREATE TABLE OBU(obu_id INTEGER PRIMARY KEY, destination TEXT);")
print("1")
cur.close()
conn.close()