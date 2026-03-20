import sqlite3

db_file = "full.db"

def get_connection():
    conn = sqlite3.connect(db_file)
    return conn