import re
import json
from sklearn import svm
import numpy
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import os
import numpy as np

def build():
    print(os.chdir("data"))
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
    # Form training data
    trainning_data = []
    trainning_label = []
    for i in range(largest_point_index):
        for data in one_hot_encoding[i]:
            trainning_data.append(data)
            trainning_label.append(i)
    trainning_data = numpy.array(trainning_data)
    trainning_label = numpy.array(trainning_label)
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
    os.chdir("..")
if __name__ == '__main__':
    build()