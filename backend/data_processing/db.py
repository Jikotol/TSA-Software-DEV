import sqlite3

db_file = "test.db"

def get_connection():
    conn = sqlite3.connect(db_file)
    return conn