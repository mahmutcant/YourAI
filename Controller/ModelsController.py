from datetime import datetime
from flask import jsonify, request, redirect,render_template
import jwt
from app import app, db
import os
from Model.User import User
from Model.SavedModel import SavedModel
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

def neuralNetwork(dataset, selectedClass, interlayers, epochNumber, userId,columns,username,modelSpecialName,droppedColumns):
    dataset = dataset.dropna(axis=0)
    label_encoder = LabelEncoder().fit(dataset[selectedClass])
    labels = label_encoder.transform(dataset[selectedClass])
    classes = list(label_encoder.classes_)
    class_len = len(dataset[selectedClass].unique())
    count_col = len(dataset.columns) - 1 
    X = dataset.drop([selectedClass], axis=1)
    Y = labels
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    Y_train = to_categorical(Y_train, num_classes=class_len)
    Y_test = to_categorical(Y_test, num_classes=class_len)
    model = Sequential()
    model.add(Dense(16, input_dim=count_col, activation="relu"))
    model.add(Dropout(0.6))
    for i in range(len(interlayers)):
        model.add(Dense(interlayers[str(i)]["neuronNumber"], activation="relu"))
        model.add(Dropout(interlayers[str(i)]["dropoutNumber"]))
    model.add(Dense(class_len, activation="softmax"))
    model.summary()
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=int(epochNumber))
    current_directory = os.getcwd()
    users_folder_path = os.path.join(current_directory, 'Users')
    usernameDirectory = os.path.join(users_folder_path, username)
    current_date = datetime.now().strftime("%Y-%m-%d")
    model_filename = f"{userId}-{modelSpecialName}-{current_date}"
    model.save(usernameDirectory + f"\{username}" + model_filename + ".h5")
    newModel = SavedModel(modelName=username+model_filename,path=usernameDirectory,userId=userId,csvData=columns,modelSpecialName=modelSpecialName,accuracyValue=max(model.history.history["accuracy"]),selectedLabel=selectedClass,listOfLabels=classes,droppedColumns=droppedColumns)
    db.session.add(newModel)
    db.session.commit()
    return max(model.history.history["accuracy"])
def knn(dataset, target, k=8):
    X = dataset.drop([target], axis=1)
    Y = dataset[target]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=15)
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    accuracy = accuracy_score(Y_test, Y_pred)
    return accuracy
def decisionTree(dataset, target):
    X = dataset.drop([target], axis=1)
    Y = dataset[target]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=15)
    model = DecisionTreeClassifier()
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    accuracy = accuracy_score(Y_test, Y_pred)
    return accuracy 
@app.route('/models', methods=['GET'])
def get_models():
    models = SavedModel.query.all()
    return jsonify(models=[model.serialize() for model in models])

def is_convertible_to_number(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        return False
@app.route('/trainModel', methods=['POST'])
def train():
    data = request.get_json()
    dataset = data.get('csvData')
    epochNumber = data.get('epochNumber')
    algorithm = data.get('algorithm')
    selectedClass = data.get('selectedClass')
    interlayers = data.get('interlayers')
    columns = data.get('columns')
    modelSpecialName = data.get('modelName')
    token = request.headers.get('Authorization').split()[1]
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    user = User.query.get(payload['user_id'])
    veri = list(dataset.values())
    selectedClassIndex = columns.index(selectedClass)
    droppedColumns = []
    newDataset = []
    for row in veri[1:]:
        new_row = []
        for i,value in enumerate(row):
            if(is_convertible_to_number(value)):
                new_value = float(value)
            else:
                if(i != selectedClassIndex):
                    if value != "" and value != "0.0" and value != "1.0" and value != "0" and value != "1" and value != 0.0 and value != 1.0 and value != 0 and value != 1:
                        droppedColumns.append(i)
                    else:
                        if value != "":
                            new_value = float(value)
            new_row.append(new_value)
        newDataset.append(new_row)
    df = pd.DataFrame(newDataset)
    clean_df = df.dropna(axis=1, how='all', inplace=False)
    if user:
        match algorithm:
            case "Perceptron":
                accuracy = neuralNetwork(clean_df,selectedClassIndex,interlayers,epochNumber,payload['user_id'],columns,user.username,modelSpecialName,list(set(droppedColumns)))
                return {"accuracy": accuracy}
            case "RNN":
                pass
            case "Karar Ağaçları":
                pass
            case "KNN":
                pass
    return 401
@app.route('/getmymodels', methods=['GET'])
def getMyModels():
    token = request.headers.get('Authorization').split()[1]
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    userId = payload["user_id"]
    models = SavedModel.query.filter_by(userId=userId).all()
    model_data = []

    for model in models:
        model_info = {
            'id': model.id,
            'modelSpecialName': model.modelSpecialName,
            'path': model.path,
            'csvData' : model.csvData,
            'accuracyValue': model.accuracyValue,
            "selectedLabel" : model.selectedLabel,
            "modelName" : model.modelName,
            "droppedColumns" : model.droppedColumns,
            "listOfLabels" : model.listOfLabels
        }
        model_data.append(model_info)
    return jsonify({"data": model_data})

@app.route('/predictModel', methods=['POST'])
def predictModel():
    data = request.get_json()
    selectedModel = data.get('selectedModel')
    inputData = data.get('inputData')
    token = request.headers.get('Authorization').split()[1]
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    user = User.query.get(payload['user_id'])
    if user:
        input_data = np.array([inputData], dtype=np.float32)
        current_directory = os.getcwd()
        users_folder_path = os.path.join(current_directory, 'Users')
        usernameDirectory = os.path.join(users_folder_path, user.username)
        model = load_model(f"{usernameDirectory}\{selectedModel}.h5")
        prediction = model.predict(input_data)
        max_index = np.argmax(prediction)
        int64_number = np.int64(max_index)
        int_number = int(int64_number)
        print(int_number)
        return jsonify({"message":int_number})
    else:
        return 401