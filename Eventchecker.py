from flask import Flask
import psycopg2
from config import host, user, password, db_name, user_id, user_mail

def Create_app():
    app = Flask(__name__)

    @app.route('/')

    def application():
        return "test"



def database():
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            datab = db_name,
            user_id = user_id,
            user_mail = user_mail
        )

    # the cursor for perfomig database operations

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )

        print(f"SERVER version: {cursor.fetchone()}")


    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")