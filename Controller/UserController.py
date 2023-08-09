import os
from flask import jsonify, request, redirect
from app import app, db
from Model.User import User
from Model.SavedModel import SavedModel
import jwt
import datetime 

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users=[user.serialize() for user in users])

@app.route('/register', methods=['POST'])
def addUser():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if not username or not password or not email:
        return jsonify({"message":"Lütfen tüm alanları doldurun"}), 400
    yeni_kullanici = User(username=username,password=password,email=email)
    db.session.add(yeni_kullanici)
    db.session.commit()
    grandparent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    users_folder_path = os.path.join(grandparent_directory, 'Users', username)
    os.makedirs(users_folder_path, exist_ok=True)
    return jsonify({'message':'Kayıt başarıyla oluşturuldu'}), 200
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"message": "Kullanıcı adı ve şifre gereklidir"}), 400
    user = User.query.filter_by(username = username).first()
    if user and user.password == password:
        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        token = jwt.encode({'user_id': user.id, 'exp': expiration}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token':token})
    else:
        return jsonify({'message':'Hatalı kullanıcı adı veya şifre'}), 401