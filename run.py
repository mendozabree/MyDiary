from api import app
from api.v1.database import DatabaseConnection


db_con = DatabaseConnection()


if __name__ == '__main__':
    app.run(debug=True)
    # db_con
    # db_con.create_table()
