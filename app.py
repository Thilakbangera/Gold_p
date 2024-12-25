import streamlit as st
import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

with open("LinearRegressionModel.pkl", "rb") as f:
    ln = pickle.load(f)

page_bg_img = '''
<style>
body {
    background-image: url("https://your-image-url-here.com/background.jpg");
    background-size: cover;
    color: white;
}
h1, h2, h3, h4, h5, h6 {
    color: gold;
    text-shadow: 2px 2px 4px #000000;
}
.stButton>button {
    background-color: gold;
    color: black;
    font-size: 18px;
    border-radius: 10px;
    border: 2px solid black;
    padding: 10px 20px;
}
.stButton>button:hover {
    background-color: black;
    color: gold;
    transition: 0.3s ease;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("Gold Price Prediction")
st.write("**Accurate predictions for the future gold prices**")

st.header("Input Historical Prices")
st.write("Enter the last 7 days of gold prices:")

last_7_days = []
for i in range(1, 8):
    price = st.number_input(f"Day {i} market Price:", min_value=0.0, step=0.01, format="%.2f",value=None)
    last_7_days.append(price)

if st.button("Predict Gold Price"):
    if len(last_7_days) == 7 and all(x > 0 for x in last_7_days):
        input_data = np.array(last_7_days).reshape(1, -1)
        predicted_price = ln.predict(input_data)
        st.success(f"Predicted Gold Price for the next day: ${predicted_price[0]:.2f}")
        # Price per ounce and per gram (in USD) after prediction
        troy_ounce_to_gram = 31.1035  # Conversion factor from troy ounce to grams
        gold_price_per_gram_usd =  predicted_price[0] / troy_ounce_to_gram  # Price per gram in USD
        gold_price_per_gram_inr = gold_price_per_gram_usd * 84.93  # Convert USD price to INR (assuming USD to INR = 82.5)
        
        # Display the price per gram in INR in green text
        st.markdown(f"<h3 style='color:green;'>Price of gold per gram in INR (calculated from prediction): ₹{gold_price_per_gram_inr:.2f}</h3>", unsafe_allow_html=True)

    else:
        st.error("Please enter valid prices for all 7 days.")

