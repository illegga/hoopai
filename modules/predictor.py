import random

def predict_game(game):
    home = game["teams"]["home"]["name"]
    away = game["teams"]["away"]["name"]

    winner = random.choice(["Home", "Away"])
    win_prob = round(random.uniform(0.60, 0.82), 3)

    line = game.get("market_line") or round(random.uniform(190, 235), 1)
    ou = random.choice(["Over", "Under"])
    p_over = round(random.uniform(0.52, 0.76), 3)
    over_odds = round(random.uniform(1.85, 2.05), 2)
    under_odds = round(random.uniform(1.85, 2.05), 2)

    edge = max(round((p_over * over_odds - 1) / over_odds if ou == "Over" else ((1 - p_over) * under_odds - 1) / under_odds, 3), 0.0)
    confidence = int((0.7 * win_prob + 0.3 * p_over) * 100)

    return {
        "predicted_winner": winner,
        "win_prob": win_prob,
        "ou_prediction": ou,
        "market_line": line,
        "p_over_percent": f"{int(p_over*100)}%",
        "over_odds": over_odds,
        "under_odds": under_odds,
        "edge": edge,
        "reasons": [
            "H2H: Last 5 → 3-2",
            f"Form: {home} 3W-2L" if winner == "Home" else f"Form: {away} 4W-1L",
            "No injuries",
            "High pace"
        ],
        "composite_score": confidence,
        "model_version": "mock-v1"
    }
