def calculate_arbitrage_opportunities(data):
    arbitrage_opportunities = []

    for match in data:
        teams = match['teams']
        sites = match['sites']
        if len(sites) < 2:
            continue

        best_odds = {}
        for site in sites:
            odds = site['odds']['h2h']
            if len(odds) != 2:
                continue
            if teams[0] not in best_odds or odds[0] > best_odds[teams[0]]:
                best_odds[teams[0]] = odds[0]
            if teams[1] not in best_odds or odds[1] > best_odds[teams[1]]:
                best_odds[teams[1]] = odds[1]

        if teams[0] in best_odds and teams[1] in best_odds:
            inv_sum = 1 / best_odds[teams[0]] + 1 / best_odds[teams[1]]
            if inv_sum < 1:
                profit_margin = (1 - inv_sum) * 100
                arbitrage_opportunities.append({
                    "Match": f"{teams[0]} vs {teams[1]}",
                    "Team A Odds": best_odds[teams[0]],
                    "Team B Odds": best_odds[teams[1]],
                    "Profit Margin": round(profit_margin, 2)
                })

    return arbitrage_opportunities
