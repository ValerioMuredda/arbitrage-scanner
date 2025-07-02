import pandas as pd

def load_data():
    # Sample mock data
    data = pd.DataFrame([
        {"Match": "Team A vs Team B", "Book A Odds": 2.1, "Book B Odds": 2.3},
        {"Match": "Team C vs Team D", "Book A Odds": 1.8, "Book B Odds": 2.3},
        {"Match": "Team E vs Team F", "Book A Odds": 2.4, "Book B Odds": 2.2},
    ])
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
