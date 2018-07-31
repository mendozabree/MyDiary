import psycopg2
import psycopg2.extras
import datetime
import time


class DatabaseConnection:
    """Class to setup database connection, cursors and """

    def __init__(self):
        """dB connection and cursors"""

        try:
            self.connection = psycopg2.connect(
                "dbname='diarydb' user='admin' host='localhost'"
                "password='diaryAdmin' port='5432'")
            self.connection.autocommit = True

            self.cursor = self.connection.cursor()
            self.dict_cursor = self.connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_users_table(self):
        """Method to create user table if none existant"""

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


class Users(DatabaseConnection):

    def register_user(self, new_user_data):
        """
        Method with sql for registering a user
        :return:
        """

        expected_key_list = ['username', 'first_name', 'last_name', 'email', 'password']

        fields_check_result = fields_check(
                    expected_key_list=expected_key_list,
                    pending_data=new_user_data
                                           )

        if not any(fields_check_result.values()):

            new_user_command = ("INSERT INTO users"\
                                "(username,first_name,last_name,email,password)"\
                                "VALUES (%s,%s,%s,%s,%s)")
            self.cursor.execute(new_user_command, (new_user_data['username'],
                                                   new_user_data['first_name'],
                                                   new_user_data['last_name'],
                                                   new_user_data['email'],
                                                   new_user_data['password']))

            return {'message': 'User successfully registered.'}, 201

        else:
            return {'message': fields_check_result}, 400

    def login_user(self, login_data):
        """
        Method with sql for logging in a user
        :return:
        """

        login_user_cmd = ("SELECT user_id FROM users WHERE"\
                          " username = %s AND"\
                          " password = %s")
        self.cursor.execute(login_user_cmd, (login_data['username'],
                                             login_data['password']))
        row = self.cursor.fetchone()
        return row


class Entries(DatabaseConnection):

    def new_entry(self, new_entry_data, current_user):
        """
        Method with sql command for new_entry
        :return:
        """
        new_entry_cmd = ("INSERT INTO entries " \
                         "(title,content,entry_date,entry_time,"
                         "entry_timestamp,user_id) " \
                         "VALUES (%s,%s,%s,%s,%s,%s)")

        entry_time = datetime.datetime.now().replace(second=0,
                                                     microsecond=0).time()
        entry_timestamp = time.time()
        self.cursor.execute(new_entry_cmd, (new_entry_data['title'],
                                            new_entry_data['content'],
                                            datetime.date.today(),
                                            entry_time,
                                            entry_timestamp,
                                            current_user))
        return True

    def all_entries(self, current_user):
        """
        Method with sql for getting all entries
        :return:
        """
        all_entries_cmd = ("SELECT title,content FROM entries "
                           "WHERE user_id = %s")
        self.dict_cursor.execute(all_entries_cmd, (current_user,))
        rows = self.dict_cursor.fetchall()
        return rows

    def get_specific(self, entry_id):
        specific_entry_cmd = ("SELECT title,content FROM entries "
                              "WHERE entry_id = %s")

        self.cursor.execute(specific_entry_cmd, entry_id)
        row = self.cursor.fetchmany(1)

        return row[0]

    def modify_entry(self, entry_id, modify_data, current_user):

        entry_time_cmd = ("SELECT entry_timestamp FROM entries WHERE "
                          "entry_id=%s AND user_id=%s")
        self.cursor.execute(entry_time_cmd, (entry_id, current_user))
        row = self.cursor.fetchone()

        creation_timestamp = float(row[0])
        current_time = time.time()

        time_diff = current_time - creation_timestamp

        if time_diff > 84600.0:
            return 'Sorry, you can no longer edit this entry.'
        else:
            modify_cmd = ("UPDATE entries SET title=%s,content=%s "
                          "WHERE user_id=%s")
            self.cursor.execute(modify_cmd, (modify_data['title'],
                                             modify_data['content'],
                                             current_user))
            return 'Updated your entry.'


def fields_check(expected_key_list, pending_data):
    messages = []
    result = dict()
    pending_data_key_list = [*pending_data.keys()]

    odds = [this_key for this_key in expected_key_list if this_key not in
            pending_data_key_list]

    if len(odds) != 0:

        for key in odds:
            error = 'Missing ' + key
            messages.append(error)
        result['code'] = 400

    similar = [some_key for some_key in expected_key_list if some_key in
               pending_data_key_list]

    for my_key in similar:
        value = pending_data[my_key]

        if value == '':
            missing_value = 'Please fill in ' + my_key
            messages.append(missing_value)
            result['code'] = 400

    result['message'] = messages

    return result

if __name__ == '__main__':
    db = DatabaseConnection()
    db.create_users_table()
    db.create_entries_table()
