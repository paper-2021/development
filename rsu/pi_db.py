# Demonstrates a simple use case of local resource access.
# This Lambda function writes a file test to a volume mounted inside
# the Lambda environment under destLRAtest. Then it reads the file and 
# publishes the content to the AWS IoT LRAtest topic. 

import sys
import greengrasssdk
import platform
import os
import logging

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Create a Greengrass Core SDK client.
client = greengrasssdk.client('iot-data')
volumePath = '/dest/LRAtest'
# /dest/DB -> ~/DB

    
def function_handler(event, context):
    client.publish(topic='DB/test', payload='Start function')
    try:
        client.publish(topic='DB/test', payload='Sent from AWS IoT Greengrass Core about DB')
        volumeInfo = os.stat(volumePath)
        client.publish(topic='DB/test', payload=str(volumeInfo))
        
        import sqlite3
        client.publish(topic='DB/test', payload='check sqlite3 import')
        
        conn = sqlite3.connect(volumePath + '/test.db')
        cur = conn.cursor()
        conn.close()
        client.publish(topic='DB/test', payload='update DB')
        
        with open(volumePath + '/db_test', 'a') as output:
            output.write('Successfully write to a file.')
        with open(volumePath + '/db_test', 'r') as myfile:
            data = myfile.read()
        client.publish(topic='DB/test', payload=data)
        
        
    except Exception as e:
        client.publish(topic='DB/test', payload='Error: '+str(e))
        logger.error('Failed to publish message: ' + str(e))
    return