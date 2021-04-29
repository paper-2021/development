#s3에 저장되어 있는 이미지 코드로 불러와서 s3의 다른 곳에 저장하기

import json
import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus

s3_client = boto3.client("s3")
s3_resocuce = boto3.resource('s3')
BUCKET_NAME = 'lchy-public'
KEY = 'image.png'

def lambda_handler(event, context):
    if event:
        print('Start!')
        tmpkey = KEY.replace('/', '')

        print('tmpkey: '+tmpkey)
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        s3_client.download_file(BUCKET_NAME, KEY , download_path)
        s3_client.upload_file( download_path, BUCKET_NAME, "sub/image.png")
        # s3_client.upload_file(lambda_path, BUCKET_NAME, "sub/result.txt")

        return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }