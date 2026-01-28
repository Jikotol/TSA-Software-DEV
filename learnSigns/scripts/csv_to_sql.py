import os
import pandas as pd
from db import get_connection
from re import findall
from handshape_utils import make_hs_freq_dict
from init_db import make_sql_tables

MAIN_GLOSSES_CMD = """
CREATE TABLE IF NOT EXISTS main_glosses (
    main_id INTEGER PRIMARY KEY, 
    main_gloss TEXT NOT NULL,
    head_gloss_id INTEGER
)
"""

GLOSSES_CMD = """
CREATE TABLE IF NOT EXISTS glosses (
    gloss_id INTEGER PRIMARY KEY, 
    main_id TEXT,
    asl_gloss TEXT NOT NULL,
    display_parts TEXT,
    notes TEXT,
    FOREIGN KEY(main_id) REFERENCES main_glosses(main_id)
)
"""

HANDSHAPES_CMD = """
CREATE TABLE IF NOT EXISTS handshapes (
    handshape_id INTEGER PRIMARY KEY, 
    gloss_id INTEGER,
    dom_start TEXT NOT NULL, 
    dom_end TEXT, 
    non_dom_start TEXT, 
    non_dom_end TEXT,
    FOREIGN KEY(gloss_id) REFERENCES glosses(gloss_id)
)
"""

COMPONENTS_CMD = """
CREATE TABLE IF NOT EXISTS components (
    components_id INTEGER PRIMARY KEY,
    gloss_id INTEGER NOT NULL,
    word1 TEXT NOT NULL,
    word2 TEXT NOT NULL,
    word3 TEXT,
    FOREIGN KEY(gloss_id) REFERENCES glosses(gloss_id)
)
"""

def input_csv_data_to_db(conn, df, hs_freq_dict):
    
    cur = conn.cursor()
    for row in df.itertuples():
        # Make gloss in glosses table
        cur.execute("INSERT INTO glosses (asl_gloss, display_parts, notes) VALUES (?, ?, ?)", (
            row.og_gloss, row.display_compound_word, row.notes
        ))
        gloss_id = cur.lastrowid
        # Retrieves the gloss' main gloss row id
        if value_exists(cur, "main_glosses", "main_gloss", row.main_gloss):
            cur.execute("SELECT main_id FROM main_glosses WHERE main_gloss=?", (row.main_gloss,))
            main_id = cur.fetchone()[0]
        else:
            # Creates a new main gloss row since it does not exist
            cur.execute("INSERT INTO main_glosses (main_gloss) VALUES (?)", (row.main_gloss,))
            main_id = cur.lastrowid
        # Updates the gloss with the right main_gloss id for linking
        # Insert gloss handshape info if available
        cur.execute("INSERT INTO handshapes (gloss_id, dom_start, dom_end, non_dom_start, non_dom_end) VALUES (?, ?, ?, ?, ?)", (
            gloss_id, 
            row.dominant_start_handshape, 
            row.dominant_end_handshape, 
            row.non_dominant_start_handshape, 
            row.non_dominant_end_handshape
        ))  

        # Insert gloss components if compound word
        if not pd.isna(row.components):
            components_list = str(row.components).split("+")
            cur.execute("INSERT INTO components (gloss_id, word1, word2, word3) VALUES (?, ?, ?, ?)", (
                gloss_id,
                components_list[0],
                components_list[1],
                components_list[2] if len(components_list) > 2 else None
            ))
        update_head_gloss_id(cur, gloss_id, main_id, hs_freq_dict)

def update_head_gloss_id(cur, gloss_id, main_id, hs_freq_dict):
    """
    Links the main_gloss and the head gloss by updating head_gloss_id in the main_glosses table. A head gloss is, usually, the simplest
    of a gloss. This means, it's not a variant, it doesn't use rare signs, and is idealy one single sign. This is used for the default
    display of the word.

    cur: sqlite3.Cursor
    gloss_id: Integer
    main_id: Integer
    rtype: None
    """
    # Get the current value of the head_id
    cur.execute("SELECT head_gloss_id FROM main_glosses WHERE main_id=?", (main_id,))
    head_id_tuple = cur.fetchone()
    if head_id_tuple and head_id_tuple[0]:
        cur.execute("UPDATE main_glosses SET head_gloss_id=? WHERE main_id=?", 
                   (get_head_gloss(cur, gloss_id, head_id_tuple[0], hs_freq_dict), main_id))
    else:
        cur.execute("UPDATE main_glosses SET head_gloss_id=? WHERE main_id=?", (gloss_id, main_id))

def value_exists(cur, table, col, value):
    query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {col} = (?))"
    cur.execute(query, (value,))
    result_tuple = cur.fetchone()

    if result_tuple and result_tuple[0] == 1:
        return True
    return False


def get_head_gloss(cur, gloss_id, head_gloss_id, hs_freq_dict):
    if compare_gloss_names(cur, gloss_id, head_gloss_id) == gloss_id:
        # Update func
        return gloss_id
    if compare_handshapes_freq(cur, gloss_id, head_gloss_id, hs_freq_dict) == gloss_id:
        return gloss_id
    return head_gloss_id
def compare_handshapes_freq(cur, gloss_id, head_gloss_id, hs_freq_dict):
    """
    handshapes: tuple
    rtype: float
    """
    cur.execute("SELECT dom_start, dom_end, non_dom_start, non_dom_end FROM handshapes WHERE gloss_id=?", (gloss_id,))
    new_gloss_handshapes = cur.fetchone()

    cur.execute("SELECT dom_start, dom_end, non_dom_start, non_dom_end FROM handshapes WHERE gloss_id=?", (head_gloss_id,))
    head_gloss_handshapes = cur.fetchone()

    if map_hs_to_freq(new_gloss_handshapes, hs_freq_dict) > map_hs_to_freq(head_gloss_handshapes, hs_freq_dict):
        return gloss_id
    return head_gloss_id
def map_hs_to_freq(handshape_tuple, hs_freq_dict):
    """
    Returns how rare the combonation of handshapes are. Returns a frequency value(0-1) where less is less common and more
    is more common.
    handshape_list: list[str]
    rtype: float
    """
    hs_appearances = 0
    for i in range(len(handshape_tuple)):
        hs = handshape_tuple[i]
        if hs and hs in hs_freq_dict:
            hs_appearances += hs_freq_dict[handshape_tuple[i]]
    return hs_appearances / len(handshape_tuple)

def compare_gloss_names(cur, new_gloss_id, head_gloss_id):
    """
    Finds the head_gloss name based on the asl gloss. Uses heuristics to decide, considering variant tags and components
    new_gloss_id: int
    head_gloss_id: int
    rtype: int
    """
    
    # Gets gloss in main_gloss table
    cur.execute("SELECT asl_gloss FROM glosses WHERE gloss_id=?", (head_gloss_id,))
    curr_head_gloss = cur.fetchone()[0]
    # Gets recently inserted gloss
    cur.execute("SELECT asl_gloss FROM glosses WHERE gloss_id=?", (new_gloss_id,))
    new_gloss = cur.fetchone()[0]

    new_var_count, head_var_count = count_variant_tags(new_gloss), count_variant_tags(curr_head_gloss)
    if new_var_count < head_var_count:
        return new_gloss_id
    return head_gloss_id

variant_tags = ["alt.", "pl", "_2", "wg", "_3", "_4", "fs-"]
def count_variant_tags(gloss):
    counter = 0
    for tag in variant_tags:
        if tag in gloss:
            counter += 1
    # favors single-sign glosses to favor them
    if "+" in gloss:
        counter += 2 # simpler gloss is preferred
    if "(" in gloss:
        pos_var_tags = findall(r"\(.\)", gloss)
        for tag in pos_var_tags:
            # 1h and 2h usually enforce uniform handedness across the sign
            if tag != "(1h)" and tag != "(2h)":
                counter += 1
    return counter

def reset_db_file(db_file):
    if os.path.exists(db_file):
        os.remove(db_file)



def main():
    table_commands = [MAIN_GLOSSES_CMD, GLOSSES_CMD, HANDSHAPES_CMD, COMPONENTS_CMD]
    reset_db_file("sample.db")
    make_sql_tables(table_commands)
    with get_connection() as conn:
        cur = conn.cursor()
        df = pd.read_csv("/Users/emerizaarce/Desktop/TSA_Software_DEV/learnSigns/data/sample.csv")
        conn.execute("BEGIN") # sqlie does all inserts in a single transaction
        input_csv_data_to_db(conn, df, make_hs_freq_dict(df))
        conn.commit()

if __name__ == "__main__":
    main()