import pandas as pd

def load_data():
   import pandas as pd
import requests
import os

def load_data():
    API_KEY = os.getenv("API_KEY")  # Your .env must contain API_KEY=your_token
    REGIONS = "us,uk"  # 'uk' overlaps with EU for most bookmakers
    URL = f"https://api.the-odds-api.com/v4/sports/upcoming/odds"

    params = {
        "api_Key": API_KEY,
        "regions": REGIONS,
        "markets": "h2h",  # head-to-head
        "oddsFormat": "decimal",
        "dateFormat": "iso"
    }

    response = requests.get(URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch odds: {response.status_code} {response.text}")

    raw_data = response.json()
    matches = []

    for event in raw_data:
        teams = event.get("teams")
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

        # Only continue if we have odds from both regions (one US, one EU/UK)
        if any(b in odds_by_book for b in ["fanduel", "draftkings", "betmgm", "pointsbetus", "wynnbet"]) and \
           any(b in odds_by_book for b in ["bet365", "bwin", "unibet", "paddypower"]):
            
            us_books = ["fanduel", "draftkings", "betmgm", "pointsbetus", "wynnbet"]
            eu_books = ["bet365", "bwin", "unibet", "paddypower"]

            # Pick one book from each region
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
    return data

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
