import unittest
import json

from api import app
from api.v1.database import DatabaseConnection


class UserTests(unittest.TestCase):

    @staticmethod
    def create_app():
        app['TESTING'] = True

    def setUp(self):

        self.user = [
            {
                'username': 'Purple',
                'first_name': 'Puppy',
                'last_name': 'Ruple',
                'email': 'purple@pty.com',
                'password': 'purple',
            }
        ]

    def tearDown(self):
        db = DatabaseConnection()
        db_cursor = db.cursor

        # db_cursor.clear()
        # db.drop

    def test_API_can_signup_user(self):
        test_user = app.test_client(self)
        response = test_user.post('/api/v1/auth/signup',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Success', str(response.data))

    def test_API_can_login_user(self):
        test_user = app.test_client(self)
        response = test_user.post('/api/v1/auth/login',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome', str(response.data))


if __name__ == '__main__':
    unittest.main()
