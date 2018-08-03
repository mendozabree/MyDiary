import unittest
from api.v1.database import DatabaseConnection


class MyTest(unittest.TestCase):

    def setUp(self):
        dbcon = DatabaseConnection()
        dbcon.create_users_table()
        dbcon.create_entries_table()

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

    def tearDown(self):
        dbcon = DatabaseConnection()
        dbcon.drop_tables()
        dbcon.close_connection()


if __name__ == '__main__':
    unittest.main()
