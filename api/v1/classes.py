from api.v1.database import DatabaseConnection

db_con = DatabaseConnection()
db_cursor = db_con.cursor


class Users:

    def __init__(self, username, first_name, last_name, email, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def register_user(self):

        add_user_query = "INSERT INTO users "\
                         "(username,first_name,last_name,email,password) "\
                         "VALUES (%s,%s,%s,%s,%s)"

        db_cursor.execute(add_user_query, (self.username, self.first_name,
                                           self.last_name, self.email,
                                           self.password))

    @staticmethod
    def login_user(login_data):

        login_user_query = "SELECT username FROM users WHERE"\
                           " username = %s AND"\
                           " password = %s"
        db_cursor.execute(login_user_query, (login_data['username'],
                                             login_data['password']))
        row = db_cursor.fetchone()
        return row


class Entries:

    def __init__(self, title, content, entry_date, entry_time):
        
        self.title = title
        self.content = content
        self.entry_date = entry_date
        self.entry_time = entry_time

    def create_entry(self):

        add_user_query = "INSERT INTO entries " \
                         "(title,content,entry_date,entry_time) " \
                         "VALUES (%s,%s,%s,%s)"

        db_cursor.execute(add_user_query, (self.title, self.content,
                                           self.entry_date, self.entry_time))
