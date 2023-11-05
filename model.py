import re
import json
from sklearn import svm
import numpy
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pickle

def one_hot_encoding(data):
    os.chdir("/mnt/d/ICSIE/wifi_positioning/data")
    data = json.loads(data)
    with open ('crucial_data.txt', 'r') as f:
        number_of_mac = int(f.readline())
        mac_list = json.loads(f.readline())
    now_wifi_list = [0] * number_of_mac
    for index in range(0, len(data)):
        mac = data[index][0]
        if(mac not in mac_list):
            continue
        strength = data[index][1]
        now_wifi_list[mac_list.index(mac)] = int(strength)
    return now_wifi_list

def build():
    os.chdir("/mnt/d/ICSIE/wifi_positioning/data")    
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
        largest_point_index = max(largest_point_index, i[0]['point']+1)
        mac_data = i[0]['macs']
        for j in range(0, len(mac_data), 2):
            mac_set.add(mac_data[j])
    print("mac_set ok")
    # Map mac to index
    mac_list = list(mac_set)
    number_of_mac = len(mac_list)
    # Form one hot encoding
    print("Start to form one hot encoding")
    one_hot_encoding = [[] for _ in range(largest_point_index)]
    for data in database:
        now_wifi_list = [0] * number_of_mac
        # print(type(data[0]))
        temp_data = data[0]['macs']
        for i in range(0, len(temp_data), 2):
            mac = temp_data[i]
            try:
                strength = int(temp_data[i+1])
            except:
                strength = 0
            now_wifi_list[mac_list.index(mac)] = strength 
        one_hot_encoding[data[0]['point']].append(now_wifi_list)
    print("one_hot_encoding ok")
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
    print(trainning_data)
    print(trainning_data.shape)
    print(trainning_label.shape)
    X_train, X_test, y_train, y_test = train_test_split(trainning_data, trainning_label, test_size=0.2)
    if largest_point_index > 1:
        # Train model
        clf = svm.LinearSVC(max_iter=1000)

        # Create the KNN classifier (specify the number of neighbors, 'n_neighbors')
        knn_classifier = KNeighborsClassifier(n_neighbors = largest_point_index)  # Example with 5 neighbors
        # Train the classifier on the training data
        knn_classifier.fit(X_train, y_train)
        # clf = knn_classifier
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
def predict(json_data):
    print("predicting")
    os.chdir("/mnt/d/ICSIE/wifi_positioning/data")
    with open('model.pkl', 'rb') as f:
        clf = pickle.load(f)
    

    one_hot_array = one_hot_encoding(json_data)
    print('---------')
    print(one_hot_array)
    print('---------')

    arr = []
    arr.append(one_hot_array)
    arr = np.array(arr)
    predict_data = clf.predict(arr)
    print("return predict data")
    print(predict_data)
    return predict_data

if __name__ == '__main__':
    build()