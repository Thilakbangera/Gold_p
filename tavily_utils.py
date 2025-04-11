import streamlit as st
import requests
from textblob import TextBlob

# Load Tavily API Key
if "TAVILY_API_KEY" not in st.secrets:
    st.error("Tavily API key is missing from Streamlit secrets!")
    TAVILY_API_KEY = ""
else:
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

HEADERS = {"Authorization": f"Bearer {TAVILY_API_KEY}"}

# 📰 Fetch Gold News Articles
def fetch_gold_news():
    url = "https://api.tavily.com/search"
    data = {
        "query": "gold price news",
        "search_depth": "basic",
        "include_answer": True
    }
    response = requests.post(url, json=data, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.warning("❌ Error fetching news.")
        return []

# 📊 Analyze sentiment of a single news article
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# 📈 Average sentiment score from recent gold news
def get_sentiment_score():
    articles = fetch_gold_news()
    sentiments = [analyze_sentiment(article.get("body", "")) for article in articles]

    sentiment_values = {"Positive": 1, "Neutral": 0, "Negative": -1}
    scores = [sentiment_values.get(s, 0) for s in sentiments]

    return sum(scores) / len(scores) if scores else 0

# 🤖 Ask a question using Tavily Q&A
def ask_tavily(question):
    url = "https://api.tavily.com/search"
    data = {
        "query": question,
        "search_depth": "basic",
        "include_answer": True
    }
    response = requests.post(url, json=data, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("answer", "No answer available.")
    else:
        return "❌ Tavily API Error"
