from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
secretKey = "XBEN6YhtZzICrrS34mNAPjgg6SlYMofx"
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = secretKey
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123qwe@localhost:5432/projects'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from Controller.UserController import *
from Controller.ModelsController import *

if __name__ == '__main__':
    app.run(debug=True) 