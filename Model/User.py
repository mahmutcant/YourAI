from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            "password" : self.password,
            "email" : self.email
        }