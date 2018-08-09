from api import app
from api.v1.database import DatabaseConnection

dbcon = DatabaseConnection()


if __name__ == '__main__':

    app.run(debug=True)
    dbcon.create_users_table()
    dbcon.create_entries_table()

