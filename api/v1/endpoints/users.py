""" This is the users module

This module contains the User endpoints, login and signup
"""

from flask_restplus import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity
import datetime

from api import api
from api.v1.serializers import user_creation_model, login_model
from ..database import User

db = User()

authorizations = {'api_key': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Bearer'
}}

# authorizations = {'Authorization': 'Bearer {}'.format(token)}

@api.route('/api/v1/auth/signup')
class Signup(Resource):
    """
    Class for signing up
    """

    @api.expect(user_creation_model)
    def post(self):
        """Method for registration of a user"""

        result = db.register_user(new_user_data=api.payload)
        return result


@api.route('/api/v1/auth/login')
class Login(Resource):
    """
    Class for logging in a registered user
    """

    @api.expect(login_model)
    def post(self):
        """Method for logging in registered user"""

        login_data = api.payload

        result = db.login_user(login_data=login_data)
        if (isinstance(result, int)):
            expires = datetime.timedelta(hours=4)
            token = create_access_token(result, expires_delta=expires)
            success = dict()
            success['status'] = 'Success'
            success['message'] = 'Welcome, to your diary {}!'.format(
                login_data['username'])
            success['token'] = token
            return {'message': success}, 200

        else:
            return result
