import requests
import pandas as pd
import os

API_KEY = os.getenv("API_KEY")

def load_data():
    url = "https://api.the-odds-api.com/v4/sports/upcoming/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    rows = []
    for match in data:
        if len(match["bookmakers"]) < 2:
            continue
        site1 = match["bookmakers"][0]["markets"][0]["outcomes"]
        site2 = match["bookmakers"][1]["markets"][0]["outcomes"]
        if len(site1) < 2 or len(site2) < 2:
            continue
        row = {
            "team1": site1[0]["name"],
            "team2": site1[1]["name"],
            "site1_team1_odds": site1[0]["price"],
            "site1_team2_odds": site1[1]["price"],
            "site2_team1_odds": site2[0]["price"],
            "site2_team2_odds": site2[1]["price"],
        }
        rows.append(row)
    return pd.DataFrame(rows)

def calculate_arbitrage_opportunities(df):
    opportunities = []
    for index, row in df.iterrows():
        odds_team1 = max(row["site1_team1_odds"], row["site2_team1_odds"])
        odds_team2 = max(row["site1_team2_odds"], row["site2_team2_odds"])
        inv_team1 = 1 / odds_team1
        inv_team2 = 1 / odds_team2
        total_inv = inv_team1 + inv_team2
        if total_inv < 1:
            profit_margin = (1 - total_inv) * 100
            opportunities.append({
                "Match": f"{row['team1']} vs {row['team2']}",
                "Best Odds Team 1": odds_team1,
                "Best Odds Team 2": odds_team2,
                "Profit Margin": round(profit_margin, 2)
            })
    return pd.DataFrame(opportunities)
