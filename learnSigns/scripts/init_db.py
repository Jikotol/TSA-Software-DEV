import sqlite3
from db import get_connection


USERS_CMD = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL
)
"""
FLASHCARD_SETS_CMD = """
CREATE TABLE IF NOT EXISTS flashcard_sets (
    set_id INTEGER PRIMARY KEY,
    set_name TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
"""
FLASHCARDS_CMD = """
CREATE TABLE IF NOT EXISTS flashcards (
    flashcard_id INTEGER PRIMARY KEY,
    set_id INTEGER NOT NULL,
    gloss_id INTEGER NOT NULL,
    FOREIGN KEY(set_id) REFERENCES flashcard_sets(set_id),
    FOREIGN KEY(gloss_id) REFERENCES glosses(gloss_id)
)
"""
VIDEOS_CMD = """
CREATE TABLE IF NOT EXISTS videos (
    video_id INTEGER PRIMARY KEY,
    youtube_url TEXT NOT NULL,
    credit TEXT NOT NULL,
    gloss_id INTEGER NOT NULL,
    FOREIGN KEY(gloss_id) REFERENCES glosses(gloss_id)
)
"""

def make_sql_tables(table_commands):
    with get_connection() as conn:
        conn.execute("BEGIN")
        cur = conn.cursor()
        for cmd in table_commands:
            cur.execute(cmd)



if __name__ == "__main__":
    table_commands = [USERS_CMD, FLASHCARD_SETS_CMD, FLASHCARDS_CMD, VIDEOS_CMD]
    make_sql_tables(table_commands)