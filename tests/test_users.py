import unittest
import json

from api import app


class UserTests(unittest.TestCase):

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

    def test_API_can_signup_user(self):
        test_user = app.test_client(self)

        response = test_user.post('/api/v1/auth/signup',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Success', str(response.data))


if __name__ == '__main__':
    unittest.main()
