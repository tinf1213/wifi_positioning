import json 
import os
from model import one_hot_encoding
from model import predict
import requests

json_data = {"point":11,"macs":["1e:08:84:a8:8f:26","99","a0:9d:c1:f0:a6:a2","16","82:7d:3a:40:03:aa","18","7a:07:b6:81:bb:8c","22","d8:07:b6:81:bb:8a","22","24:4b:fe:5f:d4:fc","35","2c:fd:a1:60:2c:dc","46","30:b7:d4:7a:72:68","57","84:0b:7c:f5:ad:88","43","f8:34:5a:74:4e:ce","24","82:7d:3a:40:0c:c4","18","60:a4:b7:5e:da:22","35","30:b7:d4:96:1d:88","20","20:76:93:55:e5:32","26"]}
point = json_data["point"]
mac_data = json_data["macs"]
data = []
for i in range(0, len(mac_data), 2):
    info = []
    info.append(mac_data[i])
    info.append(mac_data[i + 1])
    data.append(info)
json_data = json.dumps(data)
# print(json_data)
url = 'http://127.0.0.1:5000/get_position'
response = requests.post(url, json=json_data)
if response.status_code == 200:
    json_data = response.json()
    print(json_data)
else:
    print(f'Error: {response.json()["error"]}')