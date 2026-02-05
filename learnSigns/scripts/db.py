import sqlite3

db_file = "/Users/emerizaarce/Desktop/TSA_Software_DEV/learnSigns/data/full.db"
csv_file = "/Users/emerizaarce/Desktop/TSA_Software_DEV/learnSigns/data/final_data.csv"

def get_connection():
    conn = sqlite3.connect(db_file)
    return conn