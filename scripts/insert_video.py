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
    video_tuples.append((2, "https://www.youtube.com/embed/6r8HDsBMk1E?si=bD9IMQ3jHsdK7f9D&amp;start=6;end=7", "AASD Accessible Materials Project"))
    video_tuples.append((3, "https://www.youtube.com/embed/6r8HDsBMk1E?si=bD9IMQ3jHsdK7f9D&amp;start=6;end=7", "AASD Accessible Materials Project"))
    video_tuples.append((31, "https://www.youtube.com/embed/6r8HDsBMk1E?si=bD9IMQ3jHsdK7f9D&amp;start=7;end=9", "AASD Accessible Materials Project"))
    video_tuples.append((39, "https://www.youtube.com/embed/6r8HDsBMk1E?si=bD9IMQ3jHsdK7f9D&amp;start=9;end=11", "AASD Accessible Materials Project"))
    video_tuples.append((46, "https://www.youtube.com/embed/6r8HDsBMk1E?si=bD9IMQ3jHsdK7f9D&amp;start=11;end=12", "AASD Accessible Materials Project"))
    main()