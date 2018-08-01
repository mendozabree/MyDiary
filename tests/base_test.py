import unittest
from api import app
from api.v1.database import DatabaseConnection




class MyTest(unittest.TestCase):
    #
    # def create_app(self):
    #     app.config.from_object('config.TestingConfig')
    #     return app

    def setUp(self):
        dbcon = DatabaseConnection()
        dbcon.create_entries_table()
        dbcon.create_users_table()
        self.user = [
            {
                'username': 'Orange',
                'first_name': 'Puppy',
                'last_name': 'Ruple',
                'email': 'purple@pty.com',
                'password': 'purple'
            }
        ]
        self.my_user = {
            'first_name': 'Puppy',
            'last_name': 'Ruple',
            'email': 'purple@pty.com',
            'password': 'purple'
        }

        self.entries = {
                'title': 'Learning Flask',
                'content': 'Flask is a micro-framework based on python.'
                           'Flask is useful for designing APIs.'
            }

        self.entry = {
            'content': 'Flask is a micro-framework based on python.'
                       'Flask is useful for designing APIs.'
        }

    # def tearDown(self):
    #     dbcon.drop_tables()


if __name__ == '__main__':
    unittest.main()