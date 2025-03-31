import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv() 
API_TOKEN = os.getenv("API_TOKEN")  # Fetch the secret key

SENTIMENT_API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/distilbert-base-uncased-emotion"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def query_sentiment(text):
    response = requests.post(SENTIMENT_API_URL, headers=HEADERS, json={"inputs": text})
    if response.status_code == 200:
        return response.json()
    return None

def get_hotline(country):
    url = "https://blog.opencounseling.com/suicide-hotlines/"
    response = requests.get(url)
    if response.status_code != 200:
        return "Unable to fetch data."

    soup = BeautifulSoup(response.text, "html.parser")
    for section in soup.find_all("p"):
        if country.lower() in section.text.lower():
            return section.text
    return "No hotline information found."

st.title("Sentiment Care")
country = st.text_input("Which country are you from?", "")
feeling = st.text_area("How are you feeling today?", "")

if st.button("Analyze"):
    if feeling:
        sentiment = query_sentiment(feeling)
        if sentiment:
            label = sentiment[0][0]['label']
            score = sentiment[0][0]['score']
            st.write(f"**Sentiment:** {label} (Confidence: {score:.2f})")

            if label.lower() in ["sadness", "fear", "anger"]:
                hotline_info = get_hotline(country)
                st.subheader("Hotline Information:")
                st.write(hotline_info)
    else:
        st.warning("Please enter how you're feeling.")

