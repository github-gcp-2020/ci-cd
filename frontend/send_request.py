import requests
import os

PROJECT_ID=os.environ.get('PROJECT_ID', '')

URL=os.environ.get('BACKEND_URL', '')

def send_request(bucket, filename):
    try:
        req = requests.post(URL, data=filename.encode())
        print("Request response: ")
        print(req.text)

    except Exception as e:
        return "Something went wrong!"
    
    return "Success!"
