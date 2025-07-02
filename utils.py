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
    matches = []  # parsing happens later

    return raw_data


def calculate_arbitrage_opportunities(data):
    arbitrage_opportunities = []

    for match in data:
        teams = match.get('teams', [])
        sites = match.get('bookmakers', [])
        if len(sites) < 2 or len(teams) != 2:
            continue

        best_odds = {}
        for site in sites:
            odds = site.get('markets', [{}])[0].get('outcomes', [])
            if len(odds) != 2:
                continue
            for outcome in odds:
                name = outcome['name']
                price = outcome['price']
                if name not in best_odds or price > best_odds[name]:
                    best_odds[name] = price

        if len(best_odds) == 2:
            inv_sum = sum(1 / odd for odd in best_odds.values())
            if inv_sum < 1:
                profit = (1 - inv_sum) * 100
                arbitrage_opportunities.append({
                    "Match": f"{teams[0]} vs {teams[1]}",
                    "Profit Margin": round(profit, 2)
                })

    return arbitrage_opportunities
