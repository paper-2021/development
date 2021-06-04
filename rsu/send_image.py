import json
import sys

imagePath = '/src/GG/3_accident.jpg' 
url = 'http://3.35.184.173:8000/image'

def sendImage(image_path):
    try:
        import requests
        headers = {
            'accept': 'application/json'
        }
        files = {
            'file': open(image_path, 'rb')
        }
        response = requests.post(url, headers=headers, files=files)
        res_dict = response.json()
        return res_dict['image_path'] # image url
    except Exception as e :
        print("sendImage : ", str(e))
        return False