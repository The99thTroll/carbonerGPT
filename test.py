import requests
import time

#make a request to the API GET
r=requests.get("http://127.0.0.1:5000/imageWeb?url=https://google.com")
print(r.text)