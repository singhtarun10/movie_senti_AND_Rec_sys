
import streamlit as st
from PIL import Image
from sentiment_analysis import analyze_sentiment
from utils import (
    fetch_movie_details, fetch_movie_reviews, fetch_google_recommendations,
    fetch_reviews_from_ai, get_watch_verdict, fetch_movie_recommendations_from_ai,
    calculate_overall_sentiment
)

# 🎨 Theme and layout setup
st.set_page_config(
    page_title="🎬 CineSense AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom light theme styling
st.markdown("""
    <style>
        body, .stApp {
            background-color: #ffffff;
            color: #262730;
            font-family: 'Helvetica', sans-serif;
        }
        .css-1aumxhk {
            background-color: #f0f2f6 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 🧠 Title Section
st.markdown("<h1 style='text-align: center;'>Movie Sentiment & Recommendation System</h1>", unsafe_allow_html=True)
st.write("Enter the name of a movie to analyze sentiment, get summary, and discover similar recommendations.")

# 🎥 Input
movie_name = st.text_input("🎥 Movie Title")

# 🔍 Analysis Trigger
if st.button("Analyze Movie"):
    with st.spinner("Fetching movie details..."):
        movie = fetch_movie_details(movie_name)

    if movie:
        # Movie Info
        st.markdown("## 📝 Movie Info")
        st.markdown(f"**Title:** {movie['title']}")
        st.markdown(f"**Genre:** {movie['genre']}")
        st.markdown(f"**IMDb Rating:** {movie['imdb_rating']}")

        # AI Summary
        ai_review = fetch_reviews_from_ai(movie["title"])
        st.markdown("##  AI Summary & Verdict")
        st.write(f"**Summary:** {ai_review}")
        st.write(f"**Verdict:** {get_watch_verdict(movie['imdb_rating'])}")
        st.markdown("---")

        # Sentiment Summary
        all_reviews = fetch_movie_reviews(movie["id"], movie["title"])
        st.markdown("##  Overall Sentiment")
        st.write(calculate_overall_sentiment(all_reviews))
        st.markdown("---")

        # Reviews
        st.markdown("## 🧾 Top Reviews with Sentiment")
        if all_reviews:
            for index, review in enumerate(all_reviews[:10]):
                sentiment, score = analyze_sentiment(review)
                short_review = "\n".join(review.split("\n")[:4])
                st.write(f"**Review {index+1}:** *{sentiment}")
                st.markdown(f"> {short_review}...")
                st.markdown("---")
        else:
            st.warning("⚠ No reviews found.")

        # Recommendations
        st.markdown("## 🎬 Recommended Movies")
        recommendations = fetch_google_recommendations(movie["genre"])
        if not recommendations:
            recommendations = fetch_movie_recommendations_from_ai(movie["genre"])

        if recommendations:
            for rec in recommendations[:5]:
                st.markdown(f"- {rec}")
        else:
            st.warning("⚠ No recommendations found.")
    else:
        st.error("❌ Movie not found. Please try a different title.")
