from flask import Flask
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

secret_key = 'thisismysecretkey'
app.config['JWT_SECRET_KEY'] = secret_key
jwt = JWTManager(app=app)
jwt._set_error_handler_callbacks(api)
# app.config['JWT_HEADER_TYPE'] = 'JWT'

from api.v1.endpoints import users
from api.v1.endpoints import entries
