import json
import sys

imagePath = '/src/GG/3_accident.jpg' 
url = 'http://3.35.184.173:8000/image'

def sendImage():
    try:
        import requests
        headers = {
            'accept': 'application/json'
        }
        files = {
            'file': open(imagePath, 'rb')
        }
        response = requests.post(url, headers=headers, files=files)
        print('response : ', response)
        return True
    except Exception as e :
        print("sendImage : ", str(e))
        return False