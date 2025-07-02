import pandas as pd

def load_data():
    # Replace this with real API/data fetching logic
    data = pd.DataFrame([
        {"Match": "Team A vs Team B", "Book A Odds": 2.0, "Book B Odds": 2.1},
        {"Match": "Team C vs Team D", "Book A Odds": 1.8, "Book B Odds": 2.3},
    ])
    return data

def calculate_arbitrage_opportunities(data):
    opportunities = []
    for _, row in data.iterrows():
        odds_a = row["Book A Odds"]
        odds_b = row["Book B Odds"]
        if (1 / odds_a + 1 / odds_b) < 1:
            profit_margin = (1 - (1 / odds_a + 1 / odds_b)) * 100
            row["Profit Margin"] = round(profit_margin, 2)
            opportunities.append(row)
    return pd.DataFrame(opportunities)
