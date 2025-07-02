import os
print("Current working directory:", os.getcwd())

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

import streamlit as st
import pandas as pd
from .utils import load_data, calculate_arbitrage_opportunities
from telegram_alert import send_alert

st.set_page_config(page_title="EGO Arbitrage Scanner", layout="wide")
st.markdown("<h1 style='color: red;'>Welcome to EGO Arbitrage Scanner</h1>", unsafe_allow_html=True)
st.markdown("This app compares odds across sportsbooks to detect arbitrage opportunities.")

# Load and display data
data = load_data()
arbs = calculate_arbitrage_opportunities(data)

st.markdown("### 🔁 Live Arbitrage Opportunities")
st.dataframe(arbs, use_container_width=True)

# Simulate demo bankroll
if 'bankroll' not in st.session_state:
    st.session_state.bankroll = 1000
    st.session_state.bets = []

st.markdown(f"💰 Demo Bankroll: ${st.session_state.bankroll}")

# Place a simulated bet
selected_index = st.selectbox("Select match to bet on", arbs.index)
if st.button("Place Bet"):
    match = arbs.loc[selected_index]
    profit = match['Profit Margin'] * st.session_state.bankroll / 100
    st.session_state.bets.append(match.to_dict())
    st.session_state.bankroll += profit
    send_alert(f"Arbitrage bet placed: {match.to_dict()}")
    st.success(f"Bet placed! Estimated profit: ${profit:.2f}")

# Display bet history
if st.session_state.bets:
    st.markdown("### 📈 Bet History")
    st.dataframe(pd.DataFrame(st.session_state.bets))
