from flask import Flask
from flask_restplus import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

secret_key = 'thisismysecretkey'
app.config['JWT_SECRET_KEY'] = secret_key
jwt = JWTManager(app=app)

from api.v1.endpoints import users
from api.v1.endpoints import entries
