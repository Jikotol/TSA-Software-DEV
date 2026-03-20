from db import get_connection

def insert_video(cur, gloss_id, url, credit):
    cur.execute("INSERT OR IGNORE INTO videos (gloss_id, youtube_url, credit) VALUES (?, ?, ?)", 
        (gloss_id, url, credit))
    
def main():
    with get_connection() as conn:
        conn.execute("BEGIN")
        cur = conn.cursor() 
        cur.execute("DELETE FROM videos;")
        for tuple in video_tuples:
            insert_video(cur, *tuple)
        conn.commit()

if __name__ == "__main__":
    video_tuples = []
    main()