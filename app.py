import streamlit as st
import requests
from bs4 import BeautifulSoup

API_TOKEN = st.secrets["API_TOKEN"] if "API_TOKEN" in st.secrets else None

# if API_TOKEN:
#     st.success("API Token Loaded Successfully! ✅")
# else:
#     st.error("API Token Not Found! ❌ Please check Streamlit Secrets.")

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
    url = "https://blog.opencounseling.com/suicide-hotlines/"
    try:
        response = requests.get(url, timeout=10)  # Set timeout to prevent hanging
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for section in soup.find_all("p"):
            if country.lower() in section.text.lower():
                return section.text
        return "No hotline information found."
    except requests.exceptions.RequestException:
        return "Error fetching hotline data."

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

