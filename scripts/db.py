import sqlite3

db_file = "/Users/emerizaarce/Desktop/TSA Software Dev/data/full.db"
csv_file = "/Users/emerizaarce/Desktop/TSA Software Dev/data/final_data.csv"

def get_connection():
    conn = sqlite3.connect(db_file)
    return conn