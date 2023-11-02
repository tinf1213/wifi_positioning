import requests
import os

url = 'http://127.0.0.1:5000//data_update'
json_data = {'key': 'value'}  # Replace with your actual JSON data
response = requests.post(url, json=json_data)
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print(f'Error: {response.json()["error"]}')