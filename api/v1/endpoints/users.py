""" This is the users module

This module contains the User endpoints, login and signup
"""

from flask_restplus import Resource
from flask_jwt_extended import create_access_token

from api import api
from api.v1.serializers import user_creation_model, login_model
from ..classes import Users
from ..database import Users

db = Users()


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

        # output = Users.login_user(login_data=login_data)

        user_id = db.login_user(login_data=login_data)
        if user_id:
            token = create_access_token(user_id[0])
            return {'message':{'response': 'User Logged In',
                                'access-token': token}}, 200
        else:
            return {'message': 'Incorrect username or password'}, 400
