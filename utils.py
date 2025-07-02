import pandas as pd
import requests
import streamlit as st

def load_data():
    API_KEY = st.secrets["API_KEY"]
    REGIONS = "us,uk"
    URL = "https://api.the-odds-api.com/v4/sports/upcoming/odds"

    params = {
        "apiKey": API_KEY,
        "regions": REGIONS,
        "markets": "h2h",
        "oddsFormat": "decimal",
        "dateFormat": "iso"
    }

    response = requests.get(URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch odds: {response.text}")

    raw_data = response.json()
    matches = []
    # continue with rest of parsing...
