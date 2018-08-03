from flask import Flask
from flask_restplus import Api, Swagger
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app, ui=False)
Swagger(app)

# @api.route('/doc/', endpoint='doc')
# def swagger_ui():
#     return apidoc.ui_for(api)
#
# app.register_blueprint(apidoc.apidoc)

secret_key = 'thisismysecretkey'
app.config['JWT_SECRET_KEY'] = secret_key
jwt = JWTManager(app=app)
jwt._set_error_handler_callbacks(api)

from api.v1.endpoints import users
from api.v1.endpoints import entries
