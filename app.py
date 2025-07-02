import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

# Debug line: shows where the script is running from
st.write("Current working directory:", os.getcwd())

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Import functions
try:
    from utils import load_data, calculate_arbitrage_opportunities
    from telegram_alert import send_alert
except Exception as e:
    st.error(f"❌ Import failed: {e}")
    st.stop()

# Set page layout
st.set_page_config(page_title="EGO Arbitrage Scanner", layout="wide")
st.markdown("<h1 style='color: red;'>Welcome to EGO Arbitrage Scanner</h1>", unsafe_allow_html=True)
st.markdown("This app compares odds across sportsbooks to detect arbitrage opportunities.")

# Load and calculate arbitrage opportunities
