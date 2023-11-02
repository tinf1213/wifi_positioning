import os
import re
import json

os.chdir("data")
print(os.getcwd())

data = list()
with open('database.txt', 'w') as json_file:
    for i in range(1,10):
        with open('point_'+ str(i), 'r') as f:
            Lines = f.readlines()
            point_wifi_list = []
            wifi_list = []
            now_wifi = []
            for line in Lines:
                if line.find("IN-USE") == -1 and len(re.findall("(..:..:..:..:..:..)", line)) == 1:
                    mac = re.findall("(..:..:..:..:..:..)", line)[0]
                    signal = re.findall("Mbit\/s  (...)", line)[0]
                    now_wifi.append(mac)
                    now_wifi.append(int(signal))
                    wifi_list.append(now_wifi)
                    now_wifi = []
                else: #碰到新的次數
                    if len(wifi_list) == 0: # 如果wifi_list是空的就直接跳過
                        continue
                    point_wifi_list.append(wifi_list)
                    title = {"point": i}
                    wifi_list.insert(0, title)
                    json_file.write(json.dumps(wifi_list))
                    json_file.write("\n")
                    wifi_list = []