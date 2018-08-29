import psycopg2
import psycopg2.extras
import datetime
import time
import re
from werkzeug.security import generate_password_hash, check_password_hash


class DatabaseConnection:
    """Class to setup database connection, cursors and """

    def __init__(self):
        """dB connection and cursors"""
        self.connection = psycopg2.connect(
            "dbname='d4ce0ovh3865o9'"
            "user='bnpybdmuuyduqn'"
            "host='ec2-54-163-246-5.compute-1.amazonaws.com'"
            "password='1575180a621166871194e43a3ef908e4741aabb340e48b3bea28c4ddc332fe6f'"
            "port='5432'")

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
                              "password varchar(100) NOT NULL,"
                              "login_status varchar(50) NOT NULL)")
        self.cursor.execute(user_table_command)

    def create_entries_table(self):
        """Method to create user table if none existent"""

        entry_table_command = ("CREATE TABLE IF NOT EXISTS entries"
                               "(entry_id SERIAL PRIMARY KEY,"
                               "title VARCHAR(100) NOT NULL,"
                               "content VARCHAR(8000) NOT NULL,"
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
                    return {'message': fields_result}
                else:
                    new_user_command = ("INSERT INTO users"
                                        "(username,first_name,last_name,"
                                        "email,password,login_status)"
                                        "VALUES (%s,%s,%s,%s,%s,%s)")

                    user_password = generate_password_hash(
                            new_user_data['password'],
                            method='sha256'
                                                    )

                    self.cursor.execute(new_user_command,
                                        (new_user_data['username'],
                                         new_user_data['first_name'],
                                         new_user_data['last_name'],
                                         new_user_data['email'],
                                         user_password,
                                         'True'
                                         ))

                    user_id_cmd = "SELECT user_id FROM users " \
                                  "WHERE username = '{}'" \
                        .format(new_user_data['username'])

                    self.cursor.execute(user_id_cmd)
                    user = self.cursor.fetchone()
                    return user[0]

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
            login_user_cmd = "SELECT user_id,password,login_status FROM users " \
                             "WHERE username = '{}'" \
                             .format(login_data['username'])

            self.cursor.execute(login_user_cmd)
            user = self.cursor.fetchone()

            if user:
                pswd_check = check_password_hash(user[1],
                                                 login_data['password'])

                if pswd_check:
                    login_status = user[2]

                    if login_status == 'False':
                        logged_in_cmd = ("UPDATE users SET login_status='True' "
                                         "WHERE user_id={}".format(user[0]))
                        self.cursor.execute(logged_in_cmd)
                        return user[0]
                    else:
                        msg = dict()
                        msg['status'] = 'Fail'
                        msg['message'] = 'You are already logged in!'
                        return {'message': msg}, 400
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

    def update_username(self, update_data, current_user):
        get_user = "SELECT username from users WHERE username='{}'"\
                   .format(update_data['username'])
        self.cursor.execute(get_user)
        user = self.cursor.fetchone()
        if user:
            error = dict()
            error['status'] = 'Fail'
            error['message'] = 'Username is taken'
            return {'message': error}, 400
        else:
            update_query = ("UPDATE users SET username=%s "
                            "WHERE user_id=%s")
            self.cursor.execute(update_query,
                                (update_data['username'],
                                 current_user))
            msg = dict()
            msg['status'] = 'Success'
            msg['message'] = 'Username successfully updated'
            return {'message': msg}, 200

    def update_password(self, update_data, current_user):
        expected_key_list = ['current_password', 'new_password']
        fields_check_result = fields_check(expected_key_list=expected_key_list,
                                           pending_data=update_data)

        if fields_check_result:
            field_result = dict()
            field_result['status'] = 'Fail'
            field_result['message'] = fields_check_result
            return {'message': field_result}, 400
        else:
            old_password = "SELECT password from users where user_id='{}'" \
                .format(current_user)
            self.cursor.execute(old_password)
            current_password = self.cursor.fetchone()
            # print(current_password)
            pswd_check = check_password_hash(current_password[0],
                                             update_data['current_password'])

            if pswd_check:
                if update_data['current_password'] == update_data['new_password']:
                    error = dict()
                    error['status'] = 'Fail'
                    error['message'] = 'Passwords match, ' \
                                       'please enter a different password'
                    return {'message': error}, 400
                else:
                    new_password = generate_password_hash(
                            update_data['new_password'],
                            method='sha256'
                                                    )
                    update_cmd = "UPDATE users SET password=%s WHERE user_id=%s"
                    self.cursor.execute(update_cmd,
                                        (new_password,
                                         current_user))
                    success_msg = dict()
                    success_msg['status'] = 'Success'
                    success_msg['message'] = 'Password successfully updated'
                    return {'message': success_msg}, 200
            else:
                result = dict()
                result['status'] = 'Fail'
                result['message'] = 'Current password is wrong'
                return {'message': result}, 400

    def logout_user(self, current_user):
        logout_cmd = "SELECT login_status from users WHERE user_id='{}'"\
                   .format(current_user)
        self.cursor.execute(logout_cmd)
        status = self.cursor.fetchone()
        msg = dict()
        if status[0] == 'True':
            logged_out_cmd = "UPDATE users SET login_status='False' " \
                             "WHERE user_id={}".format(current_user)
            self.cursor.execute(logged_out_cmd)
            msg['status'] = 'Success'
            msg['message'] = 'You have logged out!'
            return {'message': msg}, 200
        else:
            msg['status'] = 'Fail'
            msg['message'] = 'You need to be logged in to logout!'


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

                # entry_time = datetime.datetime.now().replace(
                #             second=0, microsecond=0).time()
                entry_time = datetime.datetime.now().replace(
                            microsecond=0).time()
                entry_timestamp = time.time()

                date_now = datetime.date.today()
                format_date = date_now.strftime('%d %b %Y')

                self.cursor.execute(new_entry_cmd, (new_entry_data['title'],
                                                    new_entry_data['content'],
                                                    format_date,
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
        all_entries_cmd = ("SELECT entry_id,title,content,entry_date,entry_time,"
                           "entry_timestamp FROM entries WHERE user_id = %s")

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
        specific_entry_cmd = "SELECT title,content,entry_date,entry_time FROM entries "\
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
            entry['time'] = row[3]
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
        new_value = value.strip()
        if len(new_value) == 0:
            missing_value = 'Please fill in ' + my_key
            messages.append(missing_value)

    return messages


def is_email_valid(email):
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return True
    else:
        return False


if __name__ == '__main__':
    db = DatabaseConnection()
    db.drop_tables()
    db.create_users_table()
    db.create_entries_table()
