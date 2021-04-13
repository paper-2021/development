import sys
import greengrasssdk
import platform
import os
import logging

sys.path.append('/src/LRAtest')
# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Create a Greengrass Core SDK client.
client = greengrasssdk.client('iot-data')
volumePath = '/src/LRAtest'
# /dest/DB -> ~/DB
code ="""import sqlite3
import sys

sys.stdout = open('/src/LRAtest/output.txt', 'w')

conn = sqlite3.connect('/src/LRAtest/check.db')
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
    conn = sqlite3.connect('/src/LRAtest/check.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO " + table + " VALUES " + data)
    conn.commit()
    cur.close()
    conn.close()
    return "Sucessfully insert the data in " + table

def select_db(table):
    conn = sqlite3.connect('/src/LRAtest/check.db')
    cur = conn.cursor()
    cur.execute("SELECT * from " + table)
    return str(cur.fetchall())"""
    
def function_handler(event, context):
    client.publish(topic='DB/test', payload='Start lambda function')
    try:
        # 파이썬 파일 생성
        with open(volumePath + '/create_db.py', 'w') as output:
            output.write(code)
        client.publish(topic='DB/test', payload="complete make db file")
        
        with open(volumePath + '/create_db.py', 'r') as myfile:
            data = myfile.read()
        client.publish(topic='DB/test', payload=data)
        import create_db

        client.publish(topic='test/select/RSUState', payload=create_db.select_db('RSUState'))
        client.publish(topic='test/insert/RSUState', payload=create_db.insert_db('RSUState', "(1, 1, 1, 50, 50)"))
        client.publish(topic='test/select/RSUState', payload=create_db.select_db('RSUState'))
        
    except Exception as e:
        client.publish(topic='DB/test', payload='Error: '+str(e))
        logger.error('Failed to publish message: ' + str(e))
    return