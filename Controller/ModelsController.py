from flask import jsonify, request, redirect,render_template
from app import app, db
import os
from Model.User import User
from Model.SavedModel import SavedModel
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout

def neuralNetwork(dataset, sinif, ara_katman=25, tekrar_sayisi=20):
    label_encoder = LabelEncoder().fit(dataset[sinif])
    labels = label_encoder.transform(dataset[sinif])
    classes = list(label_encoder.classes_)
    class_len = len(dataset[sinif].unique())
    count_col = len(dataset.columns) - 1 
    X = dataset.drop([sinif], axis=1)
    Y = labels
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    Y_train = to_categorical(Y_train, num_classes=class_len)
    Y_test = to_categorical(Y_test, num_classes=class_len)
    model = Sequential()
    model.add(Dense(16, input_dim=count_col, activation="relu"))
    model.add(Dropout(0.6))
    for i in range(ara_katman):
        model.add(Dense(32, activation="relu"))
    model.add(Dropout(0.6))
    model.add(Dense(class_len, activation="softmax"))
    model.summary()
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=tekrar_sayisi)
    return max(model.history.history["accuracy"])
@app.route('/models', methods=['GET'])
def get_models():
    models = SavedModel.query.all()
    return jsonify(models=[model.serialize() for model in models])
@app.route('/upload', methods=['POST'])
def upload_csv():
    if request.method == 'POST':
        user_folder = request.form.get('user_folder')
        csv_file = request.files['csv_file']
        if user_folder and csv_file:
            user_upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_folder)
            if not os.path.exists(user_upload_folder):
                os.makedirs(user_upload_folder)
            file_path = os.path.join(user_upload_folder, csv_file.filename)
            csv_file.save(file_path)
            return jsonify({'message':'Ok'}), 200
    return jsonify({'Message':'Error'}), 500


@app.route('/trainModel', methods=['POST'])
def train(dataFrame):
    pass