import streamlit as st
import numpy as np
import pickle
from tavily_utils import fetch_gold_news, get_sentiment_score, ask_tavily

# Load model
with open("LinearRegressionModel.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="Gold Price Prediction", layout="wide")
st.title("🌟 Gold Price Prediction App")

# 📥 User Inputs
st.header("📥 Enter Last 7 Days of Gold Prices")
last_7_days = []
cols = st.columns(7)
for i, col in enumerate(cols):
    price = col.number_input(f"Day {i+1}", min_value=0.0, format="%.2f", value=None)
    last_7_days.append(price)

if st.button("📈 Predict Next Day Price"):
    if all(p is not None and p > 0 for p in last_7_days):
        input_data = np.array(last_7_days).reshape(1, -1)
        predicted_price = model.predict(input_data)[0]

        st.success(f"💰 Predicted Gold Price: ${predicted_price:.2f}")
        price_per_gram = predicted_price / 31.1035
        price_inr = price_per_gram * 84.93
        st.markdown(f"💎 Price per gram (INR): ₹{price_inr:.2f}")
    else:
        st.error("Please enter valid prices for all 7 days.")

st.markdown("---")

# 📰 News Section
st.header("📰 Live Gold News")
news_articles = fetch_gold_news()
if news_articles:
    for article in news_articles[:8]:
        title = article.get("title", "No Title")
        desc = article.get("body", "")[:200].strip() + "..."
        url = article.get("url", "#")

        st.markdown(f"### 🔗 [{title}]({url})", unsafe_allow_html=True)
        st.write(desc)
        st.markdown("---")
else:
    st.warning("No news available at the moment.")

# 📊 Sentiment
st.header("📊 Market Sentiment from News")
sentiment_score = get_sentiment_score()
if sentiment_score > 0.1:
    sentiment_text = "Positive 😊"
elif sentiment_score < -0.1:
    sentiment_text = "Negative 😟"
else:
    sentiment_text = "Neutral 😐"
st.metric("🧠 Average Sentiment", sentiment_text, f"{sentiment_score:.2f}")

st.markdown("---")

# 🤖 Tavily Q&A
st.header("🤖 Ask Tavily About Gold")
question = st.text_input("What do you want to know about gold?")
if st.button("Ask"):
    if question:
        answer = ask_tavily(question)
        st.info(answer)
    else:
        st.warning("Please enter a question.")
