from dotenv import load_dotenv
load_dotenv()

import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

from utils import load_data, calculate_arbitrage_opportunities
from telegram_alert import send_alert

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found. Make sure .env is loaded correctly.")

# Set page layout
st.set_page_config(page_title="EGO Arbitrage Scanner", layout="wide")

# Styled header
st.markdown(
    "<h1 style='color: red;'>Welcome to EGO Arbitrage Scanner</h1>",
    unsafe_allow_html=True
)
st.markdown("This app compares odds across sportsbooks to detect arbitrage opportunities.")

# Load and process data
data = load_data()
arbs = calculate_arbitrage_opportunities(data)
else:
    st.dataframe(arbs, use_container_width=True)
st.markdown("### 📊 Live Arbitrage Opportunities")
st.dataframe(arbs, use_container_width=True)

# Simulate a bankroll
if 'bankroll' not in st.session_state:
    st.session_state.bankroll = 1000
    st.session_state.bets = []

st.markdown(f"💰 **Demo Bankroll:** ${st.session_state.bankroll}")

# Bet placement
selected_index = st.selectbox("Select match to bet on", arbs.index)
if st.button("Place Bet"):
    match = arbs.loc[selected_index]
    profit_margin = match["Profit Margin"]
    profit = profit_margin * st.session_state.bankroll / 100

    st.session_state.bets.append(match.to_dict())
    st.session_state.bankroll += profit

    send_alert(f"✅ Bet placed: {match.to_dict()}")
    st.success(f"✅ Bet placed! Estimated profit: ${profit:.2f}")

# Bet history
st.markdown("### 📜 Bet History")
if st.session_state.bets:
    st.dataframe(pd.DataFrame(st.session_state.bets))
