import psycopg2
import psycopg2.extras
import datetime
import time
import re
from werkzeug.security import generate_password_hash, check_password_hash
import os


class DatabaseConnection:
    """Class to setup database connection, cursors and """

    def __init__(self):
        """dB connection and cursors"""

        app_env = os.environ.get('app_env', None)

        if app_env == 'testing':
            self.connection = psycopg2.connect(
                "dbname='diaries_testdb' user='postgres' host='localhost'"
                "password='' port='5432'")

        else:
            self.connection = psycopg2.connect(
                "dbname='diarydb' user='postgres' host='localhost'"
                "password='#5T0uch3' port='5432'")

        self.connection.autocommit = True

        self.cursor = self.connection.cursor()
        self.dict_cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

    def create_users_table(self):
        """Method to create user table if none existent"""

        user_table_command = ("CREATE TABLE IF NOT EXISTS users"
                              "(user_id SERIAL PRIMARY KEY,"
                              "username VARCHAR(100) NOT NULL,"
                              "first_name varchar(100) NOT NULL,"
                              "last_name varchar(100) NOT NULL,"
                              "email varchar(100) NOT NULL,"
                              "password varchar(100) NOT NULL)")
        self.cursor.execute(user_table_command)

    def create_entries_table(self):
        """Method to create user table if none existant"""

        entry_table_command = ("CREATE TABLE IF NOT EXISTS entries"
                               "(entry_id SERIAL PRIMARY KEY,"
                               "title VARCHAR(100) NOT NULL,"
                               "content VARCHAR(255) NOT NULL,"
                               "entry_date VARCHAR(100) NOT NULL,"
                               "entry_time VARCHAR(100) NOT NULL,"
                               "entry_timestamp VARCHAR(100) NOT NULL,"                               
                               "user_id INTEGER NOT NULL,"
                               "FOREIGN KEY (user_id)"
                               "REFERENCES  users (user_id)"
                               "ON UPDATE CASCADE ON DELETE CASCADE )")

        self.cursor.execute(entry_table_command)

    def drop_tables(self):
        drop_cmd = "DROP TABLE entries,users"
        self.cursor.execute(drop_cmd)

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


class User(DatabaseConnection):

    def register_user(self, new_user_data):
        """
        Method with sql for registering a user
        :return:
        """

        expected_key_list = ['username', 'first_name', 'last_name',
                             'email', 'password']

        fields_check_result = fields_check(
                    expected_key_list=expected_key_list,
                    pending_data=new_user_data
                                           )

        if not fields_check_result:

            if is_email_valid(email=new_user_data['email']):

                user_name_email_check = ("SELECT username,email FROM users"
                                         " WHERE username=%s OR email=%s")
                self.cursor.execute(user_name_email_check,
                                    (new_user_data['username'],
                                     new_user_data['email'])
                                    )
                                    
                row = self.cursor.fetchone()

                if row:
                    fields_result = dict()
                    fields_result['status'] = 'Fail'
                    fields_result['message'] = 'Username or email in use'
                    return {'message': fields_result}, 400
                else:
                    new_user_command = ("INSERT INTO users"
                                        "(username,first_name,last_name,"
                                        "email,password)"
                                        "VALUES (%s,%s,%s,%s,%s)")

                    user_password = generate_password_hash(
                            new_user_data['password'],
                            method='sha256'
                                                    )

                    self.cursor.execute(new_user_command,
                                        (new_user_data['username'],
                                         new_user_data['first_name'],
                                         new_user_data['last_name'],
                                         new_user_data['email'],
                                         user_password)
                                        )

                    success_msg = dict()
                    success_msg['status'] = 'Success'
                    success_msg['message'] = 'User successfully registered.'

                    return {'message': success_msg}, 201

            else:
                email_error = dict()
                email_error['status'] = 'Fail'
                email_error['message'] = 'Email is of wrong format'
                email_error['help'] = 'Format must be someone@example.com'
                return {'message': email_error}, 400

        else:
            field_fails = dict()
            field_fails['status'] = 'Fail'
            field_fails['message'] = fields_check_result
            return {'message': field_fails}, 400

    def login_user(self, login_data):
        """
        Method with sql for logging in a user
        :return:
        """

        try:
            login_user_cmd = "SELECT user_id,password FROM users " \
                             "WHERE username = '{}'" \
                             .format(login_data['username'])

            self.cursor.execute(login_user_cmd)
            user = self.cursor.fetchone()

            if user:
                pswd_check = check_password_hash(user[1],
                                                 login_data['password'])

                if pswd_check:
                    return user[0]
                else:
                    pswd_result = dict()
                    pswd_result['status'] = 'Fail'
                    pswd_result['message'] = 'Incorrect password'
                    pswd_result['help'] = 'Enter correct password'
                    return {'message': pswd_result}, 400

            else:
                user_result = dict()
                user_result['status'] = 'Fail'
                user_result['message'] = 'Incorrect username'
                user_result['help'] = 'Enter correct username'
                return {'message': user_result}, 400

        except KeyError:
            key_err_result = dict()
            key_err_result['status'] = 'Fail'
            key_err_result['message'] = 'Missing username or password'
            key_err_result['help'] = 'Please fill in missing field'
            return {"message": key_err_result}, 400


class Entry(DatabaseConnection):

    def new_entry(self, new_entry_data, current_user):
        """
        Method with sql command for new_entry
        :return:
        """

        expected_key_list = ['title', 'content']
        fields_check_result = fields_check(
            expected_key_list=expected_key_list,
            pending_data=new_entry_data)

        if fields_check_result:
            field_result = dict()
            field_result['status'] = 'Fail'
            field_result['message'] = fields_check_result
            return {'message': field_result}, 400
        else:
            title_query = "SELECT title FROM entries WHERE user_id = %s" \
                          " AND title = %s"
            self.cursor.execute(title_query, (current_user,
                                              new_entry_data['title']))
            row = self.cursor.fetchone()

            if row:
                title_error = dict()
                title_error['status'] = 'Fail'
                title_error['message'] = 'Entry with such title exists'
                title_error['help'] = 'Think of a different title'
                return title_error, 400

            else:

                new_entry_cmd = ("INSERT INTO entries "
                                 "(title,content,entry_date,entry_time,"
                                 "entry_timestamp,user_id) "
                                 "VALUES (%s,%s,%s,%s,%s,%s)")

                entry_time = datetime.datetime.now().replace(
                            second=0, microsecond=0).time()
                entry_timestamp = time.time()

                self.cursor.execute(new_entry_cmd, (new_entry_data['title'],
                                                    new_entry_data['content'],
                                                    datetime.date.today(),
                                                    entry_time,
                                                    entry_timestamp,
                                                    current_user))
                success_msg = dict()
                memory = dict()
                success_msg['status'] = 'Success'
                success_msg['message'] = 'Your memory entitled {} has been saved!'.format(
                    new_entry_data['title'])
                success_msg['your entry'] = memory
                memory['title'] = new_entry_data['title']
                memory['content'] = new_entry_data['content']
                return {'message': success_msg}, 201

    def all_entries(self, current_user):
        """
        Method with sql for getting all entries
        :return:
        """
        all_entries_cmd = ("SELECT entry_id,title,content,entry_time FROM "
                           "entries WHERE user_id = %s")

        self.dict_cursor.execute(all_entries_cmd, (current_user,))
        rows = self.dict_cursor.fetchall()
        if len(rows) == 0:
            empty_msg = dict()
            empty_msg['status'] = 'Success'
            empty_msg['message'] = 'You have no entries yet!'
            return empty_msg
        else:
            success_msg = dict()
            success_msg['status'] = 'Success'
            success_msg['message'] = rows
            return success_msg

    def get_specific(self, entry_id, current_user):
        specific_entry_cmd = "SELECT title,content,entry_date FROM entries "\
                              "WHERE entry_id = %s AND user_id = %s"

        self.cursor.execute(specific_entry_cmd, (entry_id, current_user))
        row = self.cursor.fetchone()

        if row:
            success_msg = dict()
            entry = dict()
            success_msg['status'] = 'Success'
            success_msg['entry'] = entry
            entry['title'] = row[0]
            entry['content'] = row[1]
            entry['date'] = row[2]
            return {'message': success_msg}, 200
        else:
            error_msg = dict()
            error_msg['status'] = 'Fail'
            error_msg['message'] = 'No entry found'
            error_msg['help'] = 'Enter a different id'
            return {'message': error_msg}, 404

    def modify_entry(self, entry_id, modify_data, current_user):

        expected_key_list = ['title', 'content']

        fields_check_result = fields_check(
            expected_key_list=expected_key_list,
            pending_data=modify_data)
        if fields_check_result:
            field_result = dict()
            field_result['status'] = 'Fail'
            field_result['message'] = fields_check_result
            return {'message': field_result}, 400
        else:
            entry_time_cmd = ("SELECT entry_timestamp FROM entries WHERE "
                              "entry_id=%s AND user_id=%s")
            self.cursor.execute(entry_time_cmd, (entry_id, current_user))
            row = self.cursor.fetchone()

            creation_timestamp = float(row[0])
            current_time = time.time()

            time_diff = current_time - creation_timestamp

            if time_diff > 84600.0:
                time_expired = dict()
                time_expired['status'] = 'Fail'
                time_expired['message'] = 'Sorry, you can no longer edit this entry.'
                return {'message': time_expired}, 400
            else:
                modify_cmd = ("UPDATE entries SET title=%s,content=%s "
                              "WHERE entry_id=%s AND user_id=%s")
                self.cursor.execute(modify_cmd, (modify_data['title'],
                                                 modify_data['content'],
                                                 entry_id,
                                                 current_user))
                success_msg = dict()
                success_msg['status'] = "Success"
                success_msg['message'] = 'Updated your entry.'
                success_msg['entryId'] = entry_id
                success_msg['user'] = current_user
                return {'message': success_msg}, 200


def fields_check(expected_key_list, pending_data):
    messages = []
    pending_data_key_list = [*pending_data.keys()]

    odds = [this_key for this_key in expected_key_list if this_key not in
            pending_data_key_list]

    if len(odds) != 0:

        for key in odds:
            error = 'Missing ' + key
            messages.append(error)

    similar = [some_key for some_key in expected_key_list if some_key in
               pending_data_key_list]

    for my_key in similar:
        value = pending_data[my_key]

        if value == '':
            missing_value = 'Please fill in ' + my_key
            messages.append(missing_value)

        if value == ' ':
            result = 'Empty spaces are not allowed.'
            messages.append(result)

    return messages


def is_email_valid(email):
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return True
    else:
        return False


if __name__ == '__main__':
    db = DatabaseConnection()
    db.create_users_table()
    db.create_entries_table()
