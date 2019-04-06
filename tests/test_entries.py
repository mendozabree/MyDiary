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
        token = json.loads(response.data.decode())["token"]
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

    def test_can_not_make_entry_with_existing_title(self):
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
        token = json.loads(response.data.decode())["token"]
        head = {'Authorization': 'Bearer {}'.format(token)}
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
        res = test_user.post('/api/v1/entries',
                             data=json.dumps(self.entries),
                             content_type='application/json',
                             headers=head)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Your memory entitled {} has been saved!'
                      .format(self.entries['title']), str(res.data))
        res1 = test_user.post('/api/v1/entries',
                             data=json.dumps(self.entries),
                             content_type='application/json',
                             headers=head)
        self.assertEqual(res1.status_code, 400)
        self.assertIn('Entry with such title exists', str(res1.data))

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
        token = json.loads(response.data.decode())["token"]
        head = {'Authorization': 'Bearer {}'.format(token)}
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
        res = test_user.post('/api/v1/entries',
                             data=json.dumps(self.entries),
                             content_type='application/json',
                             headers=head)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Your memory entitled {} has been saved!'
                      .format(self.entries['title']), str(res.data))

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
        token = json.loads(response.data.decode())["token"]
        head = {'Authorization': 'Bearer {}'.format(token)}
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
        result = test_user.post('/api/v1/entries',
                             data=json.dumps(self.entries),
                             content_type='application/json',
                             headers=head)
        self.assertEqual(result.status_code, 201)
        self.assertIn('Your memory entitled {} has been saved!'
                      .format(self.entries['title']), str(result.data))
        res = test_user.get('/api/v1/entries', headers=head)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Learning Flask', str(res.data))

    def test_API_will_get_msg_for_no_entries(self):
        test_user = app.test_client(self)
        response1 = test_user.post('/api/v1/auth/signup',
                                   data=json.dumps(self.user[0]),
                                   content_type='application/json')
        self.assertEqual(response1.status_code, 201)
        self.assertIn('User successfully registered.', str(response1.data))
        response = test_user.post('/api/v1/auth/login',
                                  data=json.dumps(self.user[0]),
                                  content_type='application/json')
        token = json.loads(response.data.decode())["token"]
        head = {'Authorization': 'Bearer {}'.format(token)}
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
        res = test_user.get('/api/v1/entries', headers=head)
        self.assertEqual(res.status_code, 200)
        self.assertIn('You have no entries yet!', str(res.data))

    def test_API_can_not_get_entry_with_no_id(self):
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
        token = json.loads(response.data.decode())["token"]
        head = {'Authorization': 'Bearer {}'.format(token)}
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
        result = test_user.post('/api/v1/entries',
                                data=json.dumps(self.entries),
                                content_type='application/json',
                                headers=head)
        self.assertEqual(result.status_code, 201)
        self.assertIn('Your memory entitled {} has been saved!'
                      .format(self.entries['title']), str(result.data))
        res = test_user.get('/api/v1/entries/2', headers=head)
        self.assertEqual(res.status_code, 404)
        self.assertIn('No entry found', str(res.data))

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
        token = json.loads(response.data.decode())["token"]
        head = {'Authorization': 'Bearer {}'.format(token)}
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
        result = test_user.post('/api/v1/entries',
                                data=json.dumps(self.entries),
                                content_type='application/json',
                                headers=head)
        self.assertEqual(result.status_code, 201)
        self.assertIn('Your memory entitled {} has been saved!'
                      .format(self.entries['title']), str(result.data))
        res = test_user.get('/api/v1/entries/1', headers=head)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Learning Flask', str(res.data))

    def test_API_can_not_modify_entry_with_missing_values(self):
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
        token = json.loads(response.data.decode())["token"]
        head = {'Authorization': 'Bearer {}'.format(token)}
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
        result = test_user.post('/api/v1/entries',
                                data=json.dumps(self.entries),
                                content_type='application/json',
                                headers=head)
        self.assertEqual(result.status_code, 201)
        self.assertIn('Your memory entitled {} has been saved!'
                      .format(self.entries['title']), str(result.data))
        self.entries['title'] = ''
        res1 = test_user.put('/api/v1/entries/1',
                             data=json.dumps(self.entries),
                             content_type='application/json',
                             headers=head)
        self.assertEqual(res1.status_code, 400)
        self.assertIn('Please fill in title', str(res1.data))

    # def test_API_can_not_modify_entry_after_24_hours(self):
    #     test_user = app.test_client(self)
    #     # Sign Up User
    #     response1 = test_user.post('/api/v1/auth/signup',
    #                                data=json.dumps(self.user[0]),
    #                                content_type='application/json')
    #     self.assertEqual(response1.status_code, 201)
    #     self.assertIn('User successfully registered.', str(response1.data))
    #     # Login User
    #     response = test_user.post('/api/v1/auth/login',
    #                               data=json.dumps(self.user[0]),
    #                               content_type='application/json')
    #     token = json.loads(response.data.decode())["token"]
    #     head = {'Authorization': 'Bearer {}'.format(token)}
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(token, str(response.data))
    #     # Add new entry
    #     result = test_user.post('/api/v1/entries',
    #                             data=json.dumps(self.entries),
    #                             content_type='application/json',
    #                             headers=head)
    #     self.assertEqual(result.status_code, 201)
    #     self.assertIn('Your memory entitled {} has been saved!'
    #                   .format(self.entries['title']), str(result.data))
    #     # Update timestamp of entry 1
    #     self.entries['entry_timestamp'] = 1433390252.4927907
    #     res = test_user.put('/api/v1/entries/1',
    #                         data=json.dumps(self.entries),
    #                         content_type='application/json',
    #                         headers=head)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertIn('Updated your entry.', str(res.data))
    #     # Try updating title
    #     self.entries['title'] = 'This Title'
    #     res1 = test_user.put('/api/v1/entries/1',
    #                          data=json.dumps(self.entries),
    #                          content_type='application/json',
    #                          headers=head)
    #     self.assertEqual(res1.status_code, 400)
    #     self.assertIn('Sorry, you can no longer edit this entry.', str(res1.data))

    def test_API_can_modify_entry(self):
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
        token = json.loads(response.data.decode())["token"]
        head = {'Authorization': 'Bearer {}'.format(token)}
        self.assertEqual(response.status_code, 200)
        self.assertIn(token, str(response.data))
        result = test_user.post('/api/v1/entries',
                                data=json.dumps(self.entries),
                                content_type='application/json',
                                headers=head)
        self.assertEqual(result.status_code, 201)
        self.assertIn('Your memory entitled {} has been saved!'
                      .format(self.entries['title']), str(result.data))
        self.entries['title'] = 'New Title'
        res1 = test_user.put('/api/v1/entries/1',
                             data=json.dumps(self.entries),
                             content_type='application/json',
                             headers=head)
        self.assertEqual(res1.status_code, 200)
        self.assertIn('Updated your entry', str(res1.data))
