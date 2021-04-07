import requests
import json

def function_handler(event, context):
    imagePath = '/dest/Imgtest/1_test.jpg' # image 경로 수정 필요
    url = 'http://3.35.184.173:8000/image' 
    try:
        import requests
        headers = {
            'accept': 'application/json'
        }
        files = {
            'file': open(imagePath, 'rb')
        }
        response = requests.post(url, headers=headers, files=files)
        print (response.json())
    except Exception as e :
        print("Imgtest err : ", e)
    return {
        'statusCode' : 200,
        'body' : json.dumps('Image upload success')
    }
