from flask_sqlalchemy import SQLAlchemy
from app import db

class SavedModel(db.Model):
    __tablename__ = "savedmodels"
    id = db.Column(db.Integer, primary_key=True)
    modelName = db.Column(db.String)
    path = db.Column(db.String)
    userId = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref=db.backref('models', lazy=True))