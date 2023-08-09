from flask import jsonify, request, redirect
from app import app, db
from Model.User import User
from Model.SavedModel import SavedModel

@app.route('/models', methods=['GET'])
def get_models():
    models = SavedModel.query.all()
    return jsonify(models=[model.serialize() for model in models])