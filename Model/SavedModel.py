from flask_sqlalchemy import SQLAlchemy
from app import db

class SavedModel(db.Model):
    __tablename__ = "savedmodels"
    id = db.Column(db.Integer, primary_key=True)
    modelName = db.Column(db.String)
    path = db.Column(db.String)
    userId = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref=db.backref('models', lazy=True))
    csvData = db.Column(db.JSON)
    modelSpecialName = db.Column(db.String)
    accuracyValue = db.Column(db.Float)
    selectedLabel = db.Column(db.String)
    listOfLabels = db.Column(db.JSON)
    droppedColumns = db.Column(db.JSON)