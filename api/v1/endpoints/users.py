from flask_restplus import Resource, reqparse

from api import api
from api.v1.models import DatabaseConnection
from api.v1.serializers import user_creation_model


@api.route('/api/v1/auth/signup')
class Signup(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field is required'),
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help='This field is required'),
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help='This field is required'),
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help='This field is required'),
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field is required')

    @api.expect(user_creation_model)
    def post(self):
        data = Signup.parser.parse_args()
        username = data['username']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        conn = DatabaseConnection()
        cursor = conn.cursor

        add_user_query = "INSERT INTO users (username,first_name,second_name,email,password) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(add_user_query, (username, first_name, last_name, email, password))
        return 'Success', 201
