import requests
import io
import base64
from bs4 import BeautifulSoup
from PIL import Image
from sentiment_analysis import analyze_sentiment


# ✅ Google Gemini AI Configuration (UPDATED TO `gemini-1.5-flash`)
GEMINI_API_KEY = "AIzaSyAgDHCDG1WNuW3ROCH6pytOKKGCkpwHnOw"
GEMINI_IMAGE_API = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

# ✅ TMDb API Configuration
API_KEY = "6caa82ec1f974b4d8dd7a5909e33e264"
BASE_URL = "https://api.themoviedb.org/3"



def calculate_overall_sentiment(reviews):
    """Calculate the overall sentiment distribution from a list of reviews."""
    if not reviews:
        return "No reviews available."

    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for review in reviews:
        sentiment, _ = analyze_sentiment(review)
        sentiment_counts[sentiment.split(" ")[0]] += 1  # Extract "Positive", "Negative", or "Neutral"

    total_reviews = sum(sentiment_counts.values())

    if total_reviews == 0:
        return "No sentiment data available."

    sentiment_percentages = {
        sentiment: round((count / total_reviews) * 100, 1)
        for sentiment, count in sentiment_counts.items()
    }

    return f"Overall Sentiment: Positive ({sentiment_percentages['Positive']}%), " \
           f"Negative ({sentiment_percentages['Negative']}%), " \
           f"Neutral ({sentiment_percentages['Neutral']}%)"
### 🚀 FETCH MOVIE DETAILS ###
def fetch_movie_details(movie_name):
    """Fetch movie details from TMDb API."""
    params = {"api_key": API_KEY, "query": movie_name, "language": "en-US"}
    response = requests.get(f"{BASE_URL}/search/movie", params=params)

    if response.status_code != 200:
        return None

    results = response.json().get("results", [])
    if not results:
        return None

    movie = results[0]
    description = movie.get("overview", "No description available")

    genre_id = movie.get("genre_ids")
    genre = get_genre_name(genre_id[0]) if genre_id else fetch_movie_genre_from_ai(description)

    return {
        "id": movie["id"],
        "title": movie["title"],
        "genre": genre,
        "description": description,
        "imdb_rating": movie.get("vote_average", "N/A")
    }

### 🚀 FETCH MOVIE REVIEWS (TMDb & Google Scraper) ###
def fetch_movie_reviews(movie_id, movie_title):
    """Fetch reviews from TMDb, fallback to Google scraping if missing."""
    reviews_url = f"{BASE_URL}/movie/{movie_id}/reviews"
    params = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(reviews_url, params=params)

    reviews = response.json().get("results", []) if response.status_code == 200 else []

    if not reviews:
        reviews = scrape_google_reviews(movie_title)

    return [review["content"] for review in reviews[:10]] if reviews else fetch_reviews_from_ai(movie_title)

### 🚀 GOOGLE REVIEW SCRAPER ###
def scrape_google_reviews(movie_title):
    """Scrape movie reviews from Google."""
    try:
        search_url = f"https://www.google.com/search?q={movie_title}+movie+reviews"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        reviews = []
        for result in soup.select("span"):
            text = result.get_text().strip()
            if text and len(text) > 20:
                reviews.append(text)
            if len(reviews) >= 5:
                break

        return reviews if reviews else ["No reviews found."]
    except Exception:
        return ["No reviews found."]

### 🚀 AI REVIEW & RECOMMENDATIONS ###
def fetch_reviews_from_ai(movie_title):
    """Generate a summarized review using AI."""
    ai_response = generate_ai_response(f"Summarize the movie '{movie_title}' in 5 sentences.")
    return ai_response if ai_response and len(ai_response.strip()) > 10 else "This movie has received mixed reviews. Some viewers loved it, while others found it lacking."

def fetch_movie_recommendations_from_ai(genre):
    """Use AI to suggest movie recommendations."""
    ai_response = generate_ai_response(f"Suggest 5 best movies in the {genre} genre.")
    recommendations = ai_response.split("\n")
    return [movie.strip() for movie in recommendations if movie.strip()] or ["Inception (2010)", "The Dark Knight (2008)", "Interstellar (2014)", "Shutter Island (2010)", "Fight Club (1999)"]


def fetch_google_recommendations(genre):
    """Fetch recommended movies from Google search based on genre."""
    try:
        search_url = f"https://www.google.com/search?q=best+{genre}+movies"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        recommendations = []
        for result in soup.select("h3"):
            recommendations.append(result.text.strip())
            if len(recommendations) >= 5:
                break

        return recommendations if recommendations else fetch_movie_recommendations_from_ai(genre)
    except Exception:
        return fetch_movie_recommendations_from_ai(genre)
### 🚀 AI VERDICT & MOOD BASED ON REVIEW ###
def get_watch_verdict(imdb_rating):
    """Decide if the movie is worth watching based on IMDb rating."""
    try:
        rating = float(imdb_rating)
        if rating >= 8:
            return "Must Watch! 🎬🔥"
        elif rating >=7:
            return "Recommend for watch"
        elif rating >= 5:
            return "A decent watch, but manage expectations! 🎭"
        else:
            return "You might want to skip this one... 😬"
    except ValueError:
        return "No IMDb rating available."





### 🚀 AI RESPONSE HANDLER ###
def generate_ai_response(prompt):
    """Send structured prompt to Google Gemini API."""
    try:
        headers = {"Content-Type": "application/json"}
        params = {"key": GEMINI_API_KEY}
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        response = requests.post(GEMINI_IMAGE_API, headers=headers, json=data, params=params)

        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            return "❌ AI response unavailable."
    except Exception:
        return "❌ AI response unavailable."

### 🚀 GENRE MAPPING ###
def get_genre_name(genre_id):
    """Convert genre ID to genre name using TMDb's genre mapping."""
    genre_map = {
        28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
        80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
        14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
        9648: "Mystery", 10749: "Romance", 878: "Sci-Fi", 10770: "TV Movie",
        53: "Thriller", 10752: "War", 37: "Western"
    }
    return genre_map.get(genre_id, "Unknown")
