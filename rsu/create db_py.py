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

    
def function_handler(event, context):
    client.publish(topic='DB/test', payload='Start function')
    try:
        client.publish(topic='DB/test', payload='Sent from AWS IoT Greengrass Core about DB')
        volumeInfo = os.stat(volumePath)
        client.publish(topic='DB/test', payload=str(volumeInfo))
        
        import sqlite3
        client.publish(topic='DB/test', payload='check sqlite3 import')
        
        #conn = sqlite3.connect(volumePath + '/test.db')
        #cur = conn.cursor()
        #conn.close()
        client.publish(topic='DB/test', payload='update DB')
        
        # 파이썬 파일 생성
        with open(volumePath + '/create_db.py', 'w') as output:
            output.write("""import sqlite3
import sys

sys.stdout = open('/src/LRAtest/output.txt', 'w')

conn = sqlite3.connect('/src/LRAtest/check.db')
cur = conn.cursor()
cur.execute("CREATE TABLE RSU(rsu_id INTEGER PRIMARY KEY, rsu_ip TEXT);")
cur.execute("CREATE TABLE NearRSU(rsu_id INTEGER PRIMARY KEY, FOREIGN KEY(rsu_id) REFERENCES RSU(rsu_id));")
cur.execute("CREATE TABLE RSUState(state_id INTEGER PRIMARY KEY, rsu_id INTEGER, accident_type INTEGER, accident_size INTEGER, traffic INTEGER, FOREIGN KEY(rsu_id) REFERENCES RSU(rsu_id));")
cur.execute("CREATE TABLE OBU(obu_id INTEGER PRIMARY KEY, destination TEXT);")
print("1")
cur.close()
conn.close()""")
        client.publish(topic='DB/test', payload="complete make db file")
        
        with open(volumePath + '/create_db.py', 'r') as myfile:
            data = myfile.read()
        client.publish(topic='DB/test', payload=data)
        
        import create_db
        
        
    except Exception as e:
        client.publish(topic='DB/test', payload='Error: '+str(e))
        logger.error('Failed to publish message: ' + str(e))
    return