import sqlite3
from sentiment_analysis import analyze_sentiment

# ✅ Initialize Database
def init_db():
    """Create the required database tables if they don't exist."""
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_title TEXT NOT NULL,
            review TEXT NOT NULL,
            sentiment TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# ✅ Add a User Review
def add_review(movie_title, review):
    """Store user review in the database with sentiment analysis."""
    sentiment, _ = analyze_sentiment(review)  # ✅ Analyze sentiment of the review

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO user_reviews (movie_title, review, sentiment) VALUES (?, ?, ?)",
                   (movie_title, review, sentiment))
    conn.commit()
    conn.close()

    return sentiment  # ✅ Return sentiment for UI feedback

# ✅ Get User Reviews for a Movie
def get_reviews(movie_title):
    """Fetch user reviews from the database for a given movie."""
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("SELECT review FROM user_reviews WHERE movie_title = ?", (movie_title,))
    reviews = [row[0] for row in cursor.fetchall()]

    conn.close()
    return reviews

if __name__ == "__main__":
    print("📌 Initializing database...")
    init_db()
    print("✅ Database initialized successfully!")
