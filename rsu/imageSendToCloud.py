# import sys
# from threading import Timer
# import os
import requests

volumePath = '/dest/Imgtest/'
url = 'http://3.35.184.173:8000/image' # image 경로 수정

def function_handler(event, context):
    try:
        import requests
        headers = {
            'accept': 'application/json',
            'Content-Type': 'multipart/form-data',
        }
        params = ( 
            ('anormaly_type', '1')
        )
        files = {
            'form': (open(volumePath + 'testImage.jpg', 'rb'),'image/jpg'),
        }
        response = requests.post(url, headers=headers, params=params, files=files)
        print (response.json())
    except Exception as e :
        print("Imgtest err : ", e)
    return
