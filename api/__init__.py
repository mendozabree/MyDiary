from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
api = Api(app)

from api.v1.endpoints import users
