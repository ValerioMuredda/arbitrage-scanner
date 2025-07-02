import os
import requests
def load_data():
    api_key = os.getenv("ODDS_API_KEY")
    url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds?apiKey={api_key}&regions=eu,us&markets=h2h&oddsFormat=decimal"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return []

    json_data = response.json()
    rows = []

    for match in json_data:
        teams = match['teams']
        bookmakers = match['bookmakers']

        if len(bookmakers) >= 2:
            bm1 = bookmakers[0]['markets'][0]['outcomes']
            bm2 = bookmakers[1]['markets'][0]['outcomes']

            odds1 = bm1[0]['price']
            odds2 = bm2[1]['price']

            match_name = f"{teams[0]} vs {teams[1]}"
            profit_margin = calculate_arbitrage_opportunity(odds1, odds2)

            rows.append({
                "Match": match_name,
                "Bookmaker 1 Odds": odds1,
                "Bookmaker 2 Odds": odds2,
                "Profit Margin": f"{profit_margin:.2f}%"
            })

    return rows

def calculate_arbitrage_opportunity(odds1, odds2):
    if odds1 <= 0 or odds2 <= 0:
        return 0
    inv_1 = 1 / odds1
    inv_2 = 1 / odds2
    total = inv_1 + inv_2
    if total >= 1:
        return 0
    return (1 - total) * 100
