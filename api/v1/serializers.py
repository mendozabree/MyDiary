from flask_restplus import fields

from api import api


user_creation_model = api.model('Create_My_User', {
    'username': fields.String('Your user name', description='Username'),
    'first_name': fields.String('Your first name', description='First name'),
    'last_name': fields.String('Your last name', description='User last name'),
    'email': fields.String('Your email', description='User email'),
    'password': fields.String('Your password', description='User password')
})

login_model = api.model('Login_User', {
    'username': fields.String('Your user name', description='username'),
    'password': fields.String('Your password', description='User password')
})

entry_creation_model = api.model('Create_Entry', {
    'title': fields.String('Your title', description='Entry title'),
    'content': fields.String('Your content', description='Entry content')
})

entry_get_model = api.model('Get_all_Entries', {
    'title': fields.String('Your title', description='Entry title'),
    'content': fields.String('Your content', description='Entry content'),
    'entry_date': fields.String('Your entry date', description='Entry date'),
    'entry_time': fields.String('Your entry time', description='Entry time')
})

specific_entry = api.model('Get specific Entry', {
    'title': fields.String('Your title', description='Entry title'),
    'content': fields.String('Your content', description='Entry content'),
})
