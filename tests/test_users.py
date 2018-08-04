import json

from api import app
from .base_test import MyTest


class UserTest(MyTest):

    def test_can_not_signup_user_with_missing_key(self):
        test_user = app.test_client(self)
        response = test_user.post('/api/v1/auth/signup',
                                  data=json.dumps(self.my_user),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing username', str(response.data))

    def test_can_not_signup_user_with_missing_value(self):
        test_user = app.test_client(self)
        self.user[0]['first_name'] = ''
        response = test_user.post('/api/v1/auth/signup',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please fill in first_name', str(response.data))

    def test_API_can_signup_user(self):
        test_user = app.test_client(self)
        response = test_user.post('/api/v1/auth/signup',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User successfully registered.', str(response.data))

    def test_API_can_not_login_user_with_missing_value(self):
        test_user = app.test_client(self)
        # Register user
        response = test_user.post('/api/v1/auth/signup',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User successfully registered.', str(response.data))
        # Login user
        self.user[0]['username'] = ''
        response = test_user.post('/api/v1/auth/login',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Incorrect username', str(response.data))

    def test_API_can_login_user(self):
        test_user = app.test_client(self)
        # Register user
        response = test_user.post('/api/v1/auth/signup',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User successfully registered.', str(response.data))
        # Login user
        response = test_user.post('/api/v1/auth/login',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        token = json.loads(response.data.decode())["token"]
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
