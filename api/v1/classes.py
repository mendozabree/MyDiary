# import jwt
import datetime
import time

from api.v1.database import DatabaseConnection
# from api import app

db_con = DatabaseConnection()
db_cursor = db_con.cursor
db_dict_cursor = db_con.dict_cursor


class Users:
    """
    Class for user and has the user functions that is login and sign up
    """

    def __init__(self, username, first_name, last_name, email, password):
        """Constructor for class"""

        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def register_user(self):
        """
        Method to register a user
        :return:
        """

        add_user_query = DatabaseConnection.register_user()

        db_cursor.execute(add_user_query, (self.username, self.first_name,
                                           self.last_name, self.email,
                                           self.password))

    @staticmethod
    def login_user(login_data):
        """
        Static  method to login registered users
        :param login_data:
        :return:
        """
        login_user_query = DatabaseConnection.login_user()
        db_cursor.execute(login_user_query, (login_data['username'],
                                             login_data['password']))
        row = db_cursor.fetchone()

        return row
        # if row:
        #     token = jwt.encode({'user_id': row[0],
        #                         'exp': datetime.datetime.utcnow()
        #                         + datetime.timedelta(minutes=40)},
        #                        app.config['SECRET_KEY'])
        #     user_token = token.decode('utf-8')
        #     return user_token, 200
        # else:
        #     return 'Incorrect username or password', 400


class Entries:
    """Class for entries and their methods"""
    def __init__(self, title, content, user_id):
        """Constructor"""

        self.title = title
        self.content = content
        self.entry_date = datetime.date.today()
        self.entry_time = datetime.datetime.utcnow()
        self.user_id = user_id

    def create_entry(self):
        """
        Method to create a new entry
        :return:
        """

        create_entry_query = DatabaseConnection.new_entry()

        db_cursor.execute(create_entry_query, (self.title,
                                               self.content,
                                               self.entry_date,
                                               self.entry_time,
                                               self.user_id))

    @staticmethod
    def retrieve_all_entries(user):
        """
        Method to retrieve all entries
        :param user:
        :return:
        """

        all_entries_query = DatabaseConnection.all_entries()

        db_cursor.execute(all_entries_query, [user])

        rows = db_cursor.fetchall()
        return rows

    @staticmethod
    def get_specific_entry(entry_id):

        specific_entry = DatabaseConnection.get_specific()

        db_cursor.execute(specific_entry, [entry_id])
        row = db_cursor.fetchmany(1)

        return row[0]

    @staticmethod
    def modify_entry(entry_id, modify_data, user):
        entry_time = DatabaseConnection.entry_time()

        db_dict_cursor.execute(entry_time, [entry_id, user])
        row = db_dict_cursor.fetchmany(1)

        creation_time = time.strptime(row['entry_time'], )
        expiry_time = creation_time + datetime.timedelta(hours=24)

        if expiry_time >= datetime.datetime.utcnow():
            return 'Sorry you are not allowed to update this'
        else:
            update_entry = DatabaseConnection.modify_entry()

            db_cursor.execute(update_entry, (modify_data['content'],
                                             modify_data['title'],
                                             entry_id, user))

            return 'Entry updated'
