import unittest
import json

from api import app
# from api.v1.database import DatabaseConnection


class EntriesTests(unittest.TestCase):

    @staticmethod
    def create_app():
        app['TESTING'] = True

    def setUp(self):

        self.entries = [
            {
                'title': 'Learning Flask',
                'content': 'Flask is a micro-framework based on python.'
                           'Flask is useful for designing APIs.',
                'entry_date': '18 June 2018',
                'entry_time': '22 15'
            }
        ]

    def test_API_can_make_new_entry(self):
        test_user = app.test_client(self)
        response = test_user.post('/api/v1/entries',
                                  data=json.dumps(self.entries[0]),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Success', str(response.data))

    def test_API_can_get_all_entries(self):
        test_user = app.test_client(self)
        response = test_user.get('/api/v1/entries')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Learning Flask', str(response.data))


if __name__ == '__main__':
    unittest.main()
