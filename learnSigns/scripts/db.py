import sqlite3

db_file = "/Users/emerizaarce/Desktop/TSA_Software_DEV/learnSigns/data/all_data.db"

def get_connection():
    conn = sqlite3.connect(db_file)
    return conn