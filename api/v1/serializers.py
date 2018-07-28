from flask_restplus import fields

from api import api


user_creation_model = api.model('Create_User', {
    'username': fields.String('Your user name', description='username'),
    'first_name': fields.String('Your first name', description='User first name'),
    'second_name': fields.String('Your last name', description='User last name'),
    'email': fields.String('Your email', description='User email'),
    'password': fields.String('Your password', description='User password')
})
login_model = api.model('Login_User', {
    'username': fields.String('Your user name', description='username'),
    'password': fields.String('Your password', description='User password')
})
