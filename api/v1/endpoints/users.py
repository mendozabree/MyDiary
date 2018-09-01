""" This is the users module

This module contains the User endpoints, login and signup
"""

from flask_restplus import Resource
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    create_refresh_token, jwt_refresh_token_required)
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


@api.route('/home')
class Home(Resource):
    @jwt_required
    def get(self):
        return {'message': 'Welcome user'}, 200


@api.route('/api/v1/auth/signup')
class Signup(Resource):
    """
    Class for signing up
    """

    @api.expect(user_creation_model)
    def post(self):
        """Method for registration of a user"""
        if api.payload['password'] == api.payload['confirm_password']:
            result = db.register_user(new_user_data=api.payload)
            if isinstance(result, int):
                expires = datetime.timedelta(hours=4)
                token = create_access_token(result, expires_delta=expires)
                success = dict()
                success['status'] = 'Success'
                success['message'] = 'Welcome, to your diary'
                success['access_token'] = token
                success['refresh_token'] = create_refresh_token(result)
                return {'message': success}, 201
            else:
                return result, 400
        else:
            pswd_error = dict()
            pswd_error['status'] = 'Fail'
            pswd_error['message'] = 'Passwords do not match'
            return {'message': pswd_error}, 400


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
        if isinstance(result, int):
            expires = datetime.timedelta(hours=4)
            token = create_access_token(result, expires_delta=expires)
            refresh_token = create_refresh_token(result)
            success = dict()
            success['status'] = 'Success'
            success['message'] = 'Welcome, to your diary {}!'.format(
                login_data['username'])
            success['access_token'] = token
            success['refresh_token'] = refresh_token
            return {'message': success}, 200

        else:
            return result


@api.route('/api/v1/refresh')
class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        success = dict()
        success['status'] = 'Success'
        success['message'] = 'New token created'
        success['access_token'] = create_access_token(
            identity=current_user, expires_delta=datetime.timedelta(hours=4))
        return {'message': success}, 200


@api.route('/api/v1/auth/change_username')
class UpdateUsername(Resource):
    @jwt_required
    def put(self):
        current_user = get_jwt_identity()
        result = db.update_username(update_data=api.payload,
                                    current_user=current_user)
        return result


@api.route('/api/v1/auth/change_password')
class UpdatePassword(Resource):
    @jwt_required
    def put(self):
        if api.payload['new_password'] == api.payload['confirm_password']:
            current_user = get_jwt_identity()
            result = db.update_password(update_data=api.payload,
                                        current_user=current_user)
            return result
        else:
            error = dict()
            error['status'] = 'Fail'
            error['message'] = 'New passwords do not match'
            return {'message': error}, 400


@api.route('/api/v1/logout')
class LogoutUser(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        result = db.logout_user(current_user=current_user)
        return result
