import re
import json
from sklearn import svm
import numpy
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import os
import numpy as np
import pickle

def one_hot_encoding(mac_list, data):
    now_wifi_list = [0] * len(mac_list)
    # for index in range(0, len(data)):
    #     mac = data[index][0]
    #     strength = data[index][1]
    #     now_wifi_list[mac_list.index(mac)] = strength
    return now_wifi_list

def build():
    os.chdir("data")
    print(os.getcwd())
    # Load database in
    database = []
    with open('database.txt', 'r') as json_file:
        lines = json_file.readlines()
        for line in lines:
            data = json.loads(line)
            database.append(data)
    # Create mac set & check how many points
    mac_set = set()
    largest_point_index = 0
    for i in database:
        largest_point_index = max(largest_point_index, i[0]['point'])
        for j in range(1, len(i)):
            mac_set.add(i[j][0])  
    # Map mac to index
    mac_list = list(mac_set)
    number_of_mac = len(mac_list)
    # Form one hot encoding
    one_hot_encoding = [[] for _ in range(largest_point_index)]
    for data in database:
        now_wifi_list = [0] * number_of_mac
        for index in range(1, len(data)):
            mac = data[index][0]
            strength = data[index][1]
            now_wifi_list[mac_list.index(mac)] = strength    
        one_hot_encoding[data[0]['point'] - 1].append(now_wifi_list)
    # Keep crucial data
    with open ('crucial_data.txt', 'w') as f:
        f.write(str(number_of_mac))
        f.write("\n")
        f.write(json.dumps(mac_list))
    # Form training data
    trainning_data = []
    trainning_label = []
    for i in range(largest_point_index):
        for data in one_hot_encoding[i]:
            trainning_data.append(data)
            trainning_label.append(i)
    trainning_data = numpy.array(trainning_data)
    trainning_label = numpy.array(trainning_label)
    print(trainning_data.shape)
    print(trainning_label.shape)
    X_train, X_test, y_train, y_test = train_test_split(trainning_data, trainning_label, test_size=0.2)
    # Train model
    clf = svm.LinearSVC()
    print("start to train model")
    clf.fit(X_train, y_train)
    print("trainning done")
    # Score model
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')
    # Save model
    with open('model.pkl','wb') as f:
        pickle.dump(clf,f)
    os.chdir("..")
def predict(json_data):
    os.chdir("data")
    with open ('crucial_data.txt', 'r') as f:
        number_of_mac = int(f.readline())
        mac_list = json.loads(f.readline())
    with open('model.pkl', 'rb') as f:
        clf = pickle.load(f)
    one_hot_array = one_hot_encoding(mac_list, json_data)
    arr = []
    arr.append(one_hot_array)
    arr = np.array(arr)
    predict_data = clf.predict(arr)
    os.chdir("..")
    return predict_data
# def data_clean_from_input(json_file):

if __name__ == '__main__':
    build()