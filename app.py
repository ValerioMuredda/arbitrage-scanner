
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Arbitrage Scanner", layout="wide")

st.title("Welcome to EGO Arbitrage Scanner")
st.markdown("🚀 This app compares odds across sportsbooks to detect arbitrage opportunities.")

# Placeholder demo table
data = {
    "Match": ["Team A vs Team B", "Team C vs Team D"],
    "Bookmaker 1 Odds": [2.1, 1.9],
    "Bookmaker 2 Odds": [1.8, 2.05],
    "Profit Margin": ["5.3%", "3.1%"]
}
df = pd.DataFrame(data)

st.dataframe(df)

# Placeholder for demo bankroll system
st.markdown("💰 **Demo Bankroll**: $1000")
