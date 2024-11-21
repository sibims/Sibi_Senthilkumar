import mysql.connector


def get_db_connection():
    db_connection = mysql.connector.connect(
        host="127.0.0.12",
        user="root",
        password="root",
        database="intern",
    )
    return db_connection
