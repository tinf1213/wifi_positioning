from flask import Flask, request, jsonify
from model import build
from model import predict
import os
import json
import time

app = Flask(__name__)

# Endpoint to receive JSON file
@app.route('/data_update', methods=['POST'], endpoint = 'data_update')
def receive_json():
    try:
        # Assuming the incoming request contains a JSON file
        # json_data = request.get_json()
        # print("/data_update called")
        # json_data = json.dumps(json_data)
        data = request.form
        data = str(data)
        data = data.split('@')[1]
        # print(data)
        str_info = '[' + data + ']'
        data = eval(data)
        os.chdir("/mnt/d/ICSIE/wifi_positioning/data")
        with open('database.txt', 'a') as json_file:
            json_file.write(str_info)
            json_file.write("\n")
        print("Sending calling build()")
        build()
        return jsonify({'message': 'database append successfully'}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 400

@app.route('/get_position', methods=['POST'], endpoint = 'get_position')
def receive_json():
    try:
        data = request.form
        print(type(data))
        data = str(data)
        print(type(data))     
        data = data.split('@')[1]
        data = eval(data)
        # print((data))
        # # Assuming the incoming request contains a JSON file
        # print("get_position called")
        # json_data = request.data.decode('utf-8')
        # json_data = json.loads(json_data)
        # print("/get_position called")
        # for front end
        mac_data = data['macs']
        print(mac_data)
        print("abstract macs from json")
        data = []
        for i in range(0, len(mac_data), 2):
            info = []
            info.append(mac_data[i])
            info.append(mac_data[i + 1])
            data.append(info)
        print("reformed")
        json_data = json.dumps(data)

        result = predict(json_data)
        result = str(result[0])
        return jsonify({'message': 'JSON received successfully', 'position': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    root = os.getcwd()
    app.run(debug=True)