import sqlite3
import numpy as np

DATABASE_PATH = "data/movies.db"

def recommend_movies_by_genre(genres):
    """Recommend movies based on past search history genres."""
    if not genres:
        return ["No past searches found."]
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = "SELECT title FROM movies WHERE genre IN ({seq}) LIMIT 5".format(seq=", ".join(["?"] * len(genres)))
    cursor.execute(query, genres)
    recommendations = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return recommendations if recommendations else ["No recommendations available."]

if __name__ == "__main__":
    print("Recommended Movies:", recommend_movies_by_genre(["Action", "Sci-Fi"]))
