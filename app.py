import streamlit as st
import pandas as pd
import requests

API_TOKEN = st.secrets["API_TOKEN"] if "API_TOKEN" in st.secrets else None

SENTIMENT_API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/distilbert-base-uncased-emotion"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"} if API_TOKEN else {}

def query_sentiment(text):
    if not API_TOKEN:
        return {"error": "Missing API Token"}

    response = requests.post(SENTIMENT_API_URL, headers=HEADERS, json={"inputs": text})

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        return {"error": "Invalid API Token! Check your Streamlit Secrets."}
    elif response.status_code == 429:
        return {"error": "Rate Limit Exceeded! Try again later."}
    else:
        return {"error": f"API Error {response.status_code}"}
def get_hotline(country):
    try:
        df = pd.read_excel("hotlines.xlsx")  # Load Excel file
        df.columns = df.columns.str.strip().str.lower()  # Normalize column names

        # Ensure the expected columns exist
        if "country" not in df.columns or "hotline" not in df.columns:
            return "Error: Missing required columns in the Excel file."

        # Standardize country names
        df["country"] = df["country"].str.strip().str.lower()

        hotline_info = df[df["country"] == country.strip().lower()]["hotline"]

        if not hotline_info.empty:
            return hotline_info.iloc[0]  # Return the first matching hotline
        return "No hotline information found for this country."
    except Exception as e:
        return f"Error loading hotline data: {str(e)}"

st.title("💙 Sentiment Care")
st.write("This app analyzes your emotions and provides hotline information if needed.")

country = st.text_input("🌍 Which country are you from?", "")
feeling = st.text_area("💭 How are you feeling today?", "")

if st.button("Analyze"):
    if feeling:
        sentiment = query_sentiment(feeling)

        if "error" in sentiment:
            st.error(sentiment["error"])
        else:
            label = sentiment[0][0]['label']
            score = sentiment[0][0]['score']
            st.write(f"### Sentiment: **{label}** (Confidence: {score:.2f})")

            if label.lower() in ["sadness", "fear", "anger"]:
                hotline_info = get_hotline(country)
                st.subheader("📞 Hotline Information:")
                st.write(hotline_info)
    else:
        st.warning("⚠️ Please enter how you're feeling.")
