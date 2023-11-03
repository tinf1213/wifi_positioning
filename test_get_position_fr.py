import requests
import os
import json

url = 'https://7288-140-115-50-48.ngrok.io/get_position'
json_data = {"macs":["60:45:cb:ae:a0:44","99","24:de:c6:91:f8:41","35","84:d8:1b:4a:4f:52","67","60:45:cb:ae:a0:40","96","04:42:1a:b4:03:00","57","60:63:4c:66:ab:c6","57","5c:d9:98:5f:84:00","29","24:de:c6:91:f8:46","38","24:de:c6:91:f8:45","38","24:de:c6:91:f8:40","35","94:b4:0f:d6:ff:40","43"]}
print(type(json_data))
json_data = json.dumps(json_data)
json_data = json.dumps(json_data)
  # Replace with your actual JSON data
print("Send request")
# response = requests.post(url, json=json_data)
# if response.status_code == 200:
#     json_data = response.json()
#     print(json_data)
# else:
#     print(f'Error: {response.json()["error"]}')