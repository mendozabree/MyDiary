import json

from api import app
from .base_test import MyTest


class EntryTest(MyTest):

    def test_API_can_not_make_entry_with_missing_values(self):
        test_user = app.test_client(self)
        response1 = test_user.post('/api/v1/auth/signup',
                                   data=json.dumps(self.user[0]),
                                   content_type='application/json')
        self.assertEqual(response1.status_code, 201)
        self.assertIn('User successfully registered.', str(response1.data))
        # login user
        response = test_user.post('/api/v1/auth/login',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        token = json.loads(response.data.decode('utf-8').replace("'", "/"))
        head = {'Authorization': 'Bearer {}'.format(token)}
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
        self.entries['title'] = ""
        res = test_user.post('/api/v1/entries',
                             data=json.dumps(self.entries),
                             content_type='application/json',
                             headers=head)
        self.assertEqual(res.status_code, 400)
        self.assertIn('Please fill in title', str(res.data))

    def test_API_can_make_new_entry(self):
        test_user = app.test_client(self)
        response1 = test_user.post('/api/v1/auth/signup',
                                   data=json.dumps(self.user[0]),
                                   content_type='application/json')
        self.assertEqual(response1.status_code, 201)
        self.assertIn('User successfully registered.', str(response1.data))
        # login user
        response = test_user.post('/api/v1/auth/login',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        token = json.loads(response.data.decode('utf-8').replace("'", "/"))
        head = {'Authorization': 'Bearer {}'.format(token)}
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
        res = test_user.post('/api/v1/entries',
                             data=json.dumps(self.entries),
                             content_type='application/json',
                             headers=head)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Your memory has been saved!', str(res.data))

    def test_API_can_get_all_entries(self):
        test_user = app.test_client(self)
        response1 = test_user.post('/api/v1/auth/signup',
                                   data=json.dumps(self.user[0]),
                                   content_type='application/json')
        self.assertEqual(response1.status_code, 201)
        self.assertIn('User successfully registered.', str(response1.data))
        response = test_user.post('/api/v1/auth/login',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        token = json.loads(response.data.decode('utf-8').replace("'", "/"))
        head = {'Authorization': 'Bearer {}'.format(token)}
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
        result = test_user.post('/api/v1/entries',
                             data=json.dumps(self.entries),
                             content_type='application/json',
                             headers=head)
        self.assertEqual(result.status_code, 201)
        self.assertIn('Your memory has been saved!', str(result.data))
        res = test_user.get('/api/v1/entries', headers=head)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Learning Flask', str(res.data))

    def test_API_can_get_specific_entry(self):
        test_user = app.test_client(self)
        response1 = test_user.post('/api/v1/auth/signup',
                                   data=json.dumps(self.user[0]),
                                   content_type='application/json')
        self.assertEqual(response1.status_code, 201)
        self.assertIn('User successfully registered.', str(response1.data))
        test_user = app.test_client(self)
        response = test_user.post('/api/v1/auth/login',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        token = json.loads(response.data.decode('utf-8').replace("'", "/"))
        head = {'Authorization': 'Bearer {}'.format(token)}
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
        result = test_user.post('/api/v1/entries',
                                data=json.dumps(self.entries),
                                content_type='application/json',
                                headers=head)
        self.assertEqual(result.status_code, 201)
        self.assertIn('Your memory has been saved!', str(result.data))
        res = test_user.get('/api/v1/entries', headers=head)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Learning Flask', str(res.data))
