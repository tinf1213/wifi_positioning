from flask import Flask, request, jsonify
from model import build
from model import predict
import os
import json

app = Flask(__name__)

# Endpoint to receive JSON file
@app.route('/data_update', methods=['POST'], endpoint = 'data_update')
def receive_json():
    try:
        # Assuming the incoming request contains a JSON file
        json_data = request.get_json()
        print("/data_update called")
        os.chdir("data")
        with open('database.txt', 'a') as json_file:
            json_file.write(json.dumps(json_data))
            json_file.write("\n")
        os.chdir("..")
        print("Sending calling build()")
        build()
        return jsonify({'message': 'database append successfully'}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 400

@app.route('/get_position', methods=['POST'], endpoint = 'get_position')
def receive_json():
    try:
        # Assuming the incoming request contains a JSON file
        json_data = request.get_json()
        print("/get_position called")
        # for front end
        # result = read_from_C#(json_data)
        result = predict(json.dumps(json_data))
        result = str(result[0])
        return jsonify({'message': 'JSON received successfully', 'position': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    root = os.getcwd()
    app.run(debug=True)