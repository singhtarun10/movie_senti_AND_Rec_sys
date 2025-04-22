from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Analyze sentiment of a given text using VADER and return a score."""
    sentiment_score = analyzer.polarity_scores(text)['compound']
    
    if sentiment_score >= 0.05:
        return "Positive 😀", sentiment_score
    elif sentiment_score <= -0.05:
        return "Negative 😡", sentiment_score
    else:
        return "Neutral 😐", sentiment_score

def categorize_reviews(reviews):
    """Classify reviews into Positive, Neutral, and Negative categories."""
    categorized = {"Positive": [], "Neutral": [], "Negative": []}
    
    for review in reviews:
        sentiment, _ = analyze_sentiment(review)
        if "Positive" in sentiment:
            categorized["Positive"].append(review)
        elif "Negative" in sentiment:
            categorized["Negative"].append(review)
        else:
            categorized["Neutral"].append(review)
    
    return categorized

if __name__ == "__main__":
    text = input("Enter text for sentiment analysis: ")
    sentiment, score = analyze_sentiment(text)
    print(f"Sentiment: {sentiment} (Score: {score})")
