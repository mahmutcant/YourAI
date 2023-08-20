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
        return jsonify({'id' : user.id, 'username':user.username, 'password':user.password,'name':user.name,'surname':user.surname, 'email': user.email})
    return jsonify({'error' : 'User not found'}), 404
@app.route('/changepassword', methods=["PUT"])
def changeUserPassword():
    token = request.headers.get('Authorization').split()[1]
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    user = User.query.get(payload['user_id'])
    data = request.get_json()
    if user:
        try:
            user.password = data.get('newPassword')
            db.session.commit()
            return jsonify({"message":"Basarili"}), 200
        except:
            db.session.rollback()
            return jsonify({'error': "Hata"}), 400
@app.route('/changeuserinfo', methods=["PUT"])
def changeUserInfo():
    token = request.headers.get('Authorization').split()[1]
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    user = User.query.get(payload['user_id'])
    data = request.get_json()
    path = "C:/Users/mahca/OneDrive/Masaüstü/BitirmeProjesi/Users/" + user.username
    if user:
        try:
            eski_klasor_yolu = path
            yeni_klasor_yolu = os.path.join(os.path.dirname(path), data.get('username'))
            os.rename(eski_klasor_yolu, yeni_klasor_yolu)

            user.name = data.get('name')
            user.surname = data.get('surname')
            user.username = data.get('username')
            user.email = data.get('email')
            db.session.commit()

            return jsonify({'message':'Kullanıcı bilgileri güncellendi'}), 200
        except:
            db.session.rollback()
            return jsonify({'error': "Hata"}), 400