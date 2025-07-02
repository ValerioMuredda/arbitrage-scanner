import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def load_data():
    import streamlit as st
API_KEY = st.secrets["API_KEY"]

    REGIONS = "us,uk"
    URL = "https://api.the-odds-api.com/v4/sports/upcoming/odds"

    params = {
        "api_key": API_KEY,
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

    for event in raw_data:
        teams = event.get("teams", [])
        bookmakers = event.get("bookmakers", [])

        odds_by_book = {}
        for book in bookmakers:
            key = book.get("key")
            markets = book.get("markets", [])
            for market in markets:
                if market.get("key") == "h2h":
                    outcomes = market.get("outcomes", [])
                    if len(outcomes) == 2:
                        odds_by_book[key] = [o["price"] for o in outcomes]

     
        if any(b in odds_by_book for b in ["fanduel", "draftkings", "betmgm", "pointsbetus", "wynnbet"]) and \
           any(b in odds_by_book for b in ["bet365", "bwin", "unibet", "paddypower"]):

            us_books = ["fanduel", "draftkings", "betmgm", "pointsbetus", "wynnbet"]
            eu_books = ["bet365", "bwin", "unibet", "paddypower"]

            book_a = next((b for b in us_books if b in odds_by_book), None)
            book_b = next((b for b in eu_books if b in odds_by_book), None)

            if book_a and book_b:
                odds_a = odds_by_book[book_a]
                odds_b = odds_by_book[book_b]
                matches.append({
                    "Match": f"{teams[0]} vs {teams[1]}",
                    "Book A Odds": odds_a[0],
                    "Book B Odds": odds_b[1]
                })

    return pd.DataFrame(matches)


def calculate_arbitrage_opportunities(data):
    opportunities = []
    for _, row in data.iterrows():
        a = row["Book A Odds"]
        b = row["Book B Odds"]
        profit_margin = (1 - (1/a + 1/b)) * 100
        if profit_margin > 0:
            row["Profit Margin"] = round(profit_margin, 2)
            opportunities.append(row)
    return pd.DataFrame(opportunities)
