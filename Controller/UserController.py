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
@app.route('/protected', methods=['GET'])
def protected_route():
    token = request.headers.get('Authorization').split()[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f'Hello, {payload["user_id"]}! This is a protected route.'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

@app.route('/register', methods=['POST'])
def addUser():
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    yeni_kullanici = User(name = name,surname = surname,username=username,password=password,email=email)
    try:
        db.session.add(yeni_kullanici)
        db.session.commit()
        grandparent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        users_folder_path = os.path.join(grandparent_directory, 'Users', username)
        os.makedirs(users_folder_path, exist_ok=True)
        return jsonify({'message':'Kayıt başarıyla oluşturuldu'}), 200
    except:
        return jsonify({'message':'Başarısız'}), 500
    
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
    
@app.route('/getuserinfo', methods=['GET'])
def getUserInfo():
    token = request.headers.get('Authorization').split()[1]
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    user = User.query.get(payload['user_id'])
    if user:
        return jsonify({'user_id' : user.id, 'username':user.name, 'password':user.password, 'email': user.email})
    return jsonify({'error' : 'User not found'}), 404
        