from flask import jsonify, request, redirect
from app import app, db
from Model.User import User
from Model.SavedModel import SavedModel

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
    return jsonify({'message':'Kayıt başarıyla oluşturuldu'}), 200
