import requests
import os
from textblob import TextBlob
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
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
        print("❌ Error fetching news:", response.text)
        return []

import requests
import os
from textblob import TextBlob
from dotenv import load_dotenv

# Load API Key
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
HEADERS = {"Authorization": f"Bearer {TAVILY_API_KEY}"}

# 📰 Fetch Gold News
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
        print("Error fetching news:", response.text)
        return []

# 📊 Analyze Sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# 📈 Sentiment Score
def get_sentiment_score():
    articles = fetch_gold_news()
    sentiments = [analyze_sentiment(article.get("body", "")) for article in articles]
    values = {"Positive": 1, "Neutral": 0, "Negative": -1}
    scores = [values.get(s, 0) for s in sentiments]
    return sum(scores) / len(scores) if scores else 0

# 🤖 Tavily Q&A
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
        print("Q&A error:", response.text)
        return "Tavily API Error"

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

    if scores:
        return sum(scores) / len(scores)
    else:
        return 0


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
        print("❌ Error in Q&A:", response.text)
        return "Tavily API Error"
