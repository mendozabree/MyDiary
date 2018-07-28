""" This is the users module

This module contains the User endpoints, login and signup
"""

from flask_restplus import Resource
# from flask_jwt_extended import create_access_token

from api import api
from api.v1.database import DatabaseConnection
from api.v1.serializers import user_creation_model, login_model
from ..classes import Users

# instance of database connection
conn = DatabaseConnection()
cursor = conn.cursor


@api.route('/api/v1/auth/signup')
class Signup(Resource):
    """
    Class for signing up
    """

    @api.expect(user_creation_model)
    def post(self):
        """Post method for a new user"""

        new_user_data = api.payload

        new_user = Users(username=new_user_data['username'],
                         first_name=new_user_data['first_name'],
                         last_name=new_user_data['last_name'],
                         email=new_user_data['email'],
                         password=new_user_data['password'])
        new_user.register_user()

        return 'Success', 201


@api.route('/api/v1/auth/login')
class Login(Resource):
    """
    Class for logging in a registered user
    """

    @api.expect(login_model)
    def post(self):
        """POST method for logging in user"""

        login_data = api.payload

        Users.login_user(login_data=login_data)

        # auth_token = create_access_token(row)

        return 'Welcome', 200
