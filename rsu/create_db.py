# 데이터 베이스를 생성해서 output을 output.txt에 넣는 코드
import sqlite3


conn = sqlite3.connect('check.db')
cur = conn.cursor()

try:
    cur.execute("CREATE TABLE RSU(rsu_id INTEGER PRIMARY KEY, rsu_ip TEXT);")
    cur.execute("CREATE TABLE NearRSU(rsu_id INTEGER PRIMARY KEY, FOREIGN KEY(rsu_id) REFERENCES RSU(rsu_id));")
    cur.execute("CREATE TABLE RSUState(state_id INTEGER PRIMARY KEY, rsu_id INTEGER, accident_type INTEGER, accident_size INTEGER, traffic INTEGER, FOREIGN KEY(rsu_id) REFERENCES RSU(rsu_id));")
    cur.execute("CREATE TABLE OBU(obu_id INTEGER PRIMARY KEY, destination TEXT);")
    cur.close()
    conn.close()
except sqlite3.OperationalError:
    print('table color already exist')

# 데이터 베이스에 집어 넣는 프로그램
def insert_db(table, data):
    conn = sqlite3.connect('check.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO " + table + " VALUES " + data)
    conn.commit()
    cur.close()
    conn.close()
    return "Sucessfully insert the data in " + table

def select_db(table):
    conn = sqlite3.connect('check.db')
    cur = conn.cursor()
    cur.execute("SELECT * from " + table)
    return str(cur.fetchall())
"""
print(select_db('RSU'))
print(insert_db('RSU', "(1234, '192.168.195')"))
print(select_db('RSU'))
"""