import json
import sys
import greengrasssdk
import platform
import os
import logging

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client("iot-data")

def function_handler(event, context):
    imagePath = '/dest/Imgtest/1_test.jpg' # image 경로 수정 필요
    url = 'http://3.35.184.173:8000/image'
    client.publish(topic="test/image", payload = 'Sent from AWS IoT GG Core 1')
    try:
        client.publish(topic="test/image", payload = 'Sent from AWS IoT GG Core 2')
        import requests
        client.publish(topic="test/image", payload = 'Import requests success')
        headers = {
            'accept': 'application/json'
        }
        files = {
            'file': open(imagePath, 'rb')
        }
        client.publish(topic="test/image", payload = 'Set headers, files success')
        response = requests.post(url, headers=headers, files=files)
        client.publish(topic="test/image", payload = 'Post success')
        # print (response.json())
        client.publish(topic="test/image", payload = str(response.json()))
        client.publish(topic="test/image", payload = 'Send Image success')
    except Exception as e :
        client.publish(topic="test/image", payload = 'Send image error')
        client.publish(topic="test/image", payload = str(e))
        logger.error('Failed to publish msg : ' + repr(e))
        # print("Imgtest err : ", e)
    return
