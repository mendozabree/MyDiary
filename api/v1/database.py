import psycopg2
import psycopg2.extras


class DatabaseConnection:
    """
    Class to setup database connection and the cursors
    """

    def __init__(self):

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
                                "content varchar(255) NOT NULL,"
                                "entry_date varchar(100) NOT NULL,"
                                "entry_time varchar(100) NOT NULL)")

        self.cursor.execute(entry_table_command)


if __name__ == '__main__':
    db = DatabaseConnection()
    db.create_users_table()
    db.create_entries_table()
