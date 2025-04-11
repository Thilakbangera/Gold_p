import requests
import streamlit as st
from textblob import TextBlob

# Load API key from Streamlit secrets
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

# 📰 Fetch latest gold-related news
def fetch_gold_news():
    url = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}
    params = {
        "query": "gold price news",
        "max_results": 8
    }

    response = requests.post(url, json=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        st.error(f"Error fetching news: {response.status_code}")
        return []

# 📊 Compute sentiment score from news articles
def get_sentiment_score():
    articles = fetch_gold_news()
    scores = []

    for article in articles:
        text = article.get("body", "")
        if text:
            blob = TextBlob(text)
            scores.append(blob.sentiment.polarity)

    return sum(scores) / len(scores) if scores else 0.0

# 🤖 Ask Tavily a custom question
def ask_tavily(question):
    url = "https://api.tavily.com/ask"
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}
    data = {"query": question}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json().get("answer", "No answer found.")
    else:
        return f"Error: {response.status_code} - {response.text}"
