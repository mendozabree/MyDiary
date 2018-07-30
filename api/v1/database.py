import psycopg2
import psycopg2.extras


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
                               "user_id INTEGER NOT NULL,"
                               "FOREIGN KEY (user_id)"
                               "REFERENCES  users (user_id)"
                               "ON UPDATE CASCADE ON DELETE CASCADE )")

        self.cursor.execute(entry_table_command)

    @staticmethod
    def register_user():
        """
        Method with sql for registering a user
        :return:
        """
        new_user_command = ("INSERT INTO users"\
                            "(username,first_name,last_name,email,password)"\
                            "VALUES (%s,%s,%s,%s,%s)")
        return new_user_command

    @staticmethod
    def login_user():
        """
        Method with sql for logging in a user
        :return:
        """

        login_user_cmd = ("SELECT user_id FROM users WHERE"\
                          " username = %s AND"\
                          " password = %s")
        return login_user_cmd

    @staticmethod
    def new_entry():
        """
        Method with sql command for new_entry
        :return:
        """
        new_entry_cmd = ("INSERT INTO entries " \
                         "(title,content,entry_date,entry_time,user_id) " \
                         "VALUES (%s,%s,%s,%s,%s)")
        return new_entry_cmd

    @staticmethod
    def all_entries():
        """
        Method with sql for getting all entries
        :return:
        """
        all_entries_cmd = ("SELECT title,content FROM entries "
                           "WHERE user_id = %s")
        return all_entries_cmd

    @staticmethod
    def get_specific():
        specific_entry_cmd = ("SELECT title,content FROM entries "
                              "WHERE entry_id = %s")

        return specific_entry_cmd

    @staticmethod
    def entry_time():
        entry_time_cmd = ("SELECT entry_time FROM entries WHERE "
                          "entry_id=%s AND user_id=%s")

        return entry_time_cmd

    @staticmethod
    def modify_entry():
        modify_entry_cmd = ("UPDATE entries SET content=%s,title=%s WHERE"
                            "entry_id=%s AND user_id=%s ")

        return modify_entry_cmd


if __name__ == '__main__':
    db = DatabaseConnection()
    db.create_users_table()
    db.create_entries_table()
