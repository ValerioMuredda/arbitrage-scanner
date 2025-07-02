
import pandas as pd

def load_data():
    # Placeholder simulated data
    return pd.DataFrame([
        {"Match": "Team A vs Team B", "Bookmaker 1 Odds": 2.1, "Bookmaker 2 Odds": 1.8},
        {"Match": "Team C vs Team D", "Bookmaker 1 Odds": 1.9, "Bookmaker 2 Odds": 2.05},
    ])

def calculate_arbitrage_opportunities(df):
    df['Profit Margin'] = ((1 / df['Bookmaker 1 Odds']) + (1 / df['Bookmaker 2 Odds']) - 1) * -100
    df = df[df['Profit Margin'] > 0].reset_index(drop=True)
    return df
