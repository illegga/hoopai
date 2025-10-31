# modules/predictor.py
import random
from datetime import datetime

def predict_game(game):
    """
    Input: raw game dict from API (has id, date, teams, league)
    Output: prediction dict for prediction_card()
    """
    # --- BASIC INFO ---
    home = game["teams"]["home"]["name"]
    away = game["teams"]["away"]["name"]
    league = game.get("league", {}).get("name", "Unknown")

    # --- MOCK PREDICTION (replace later with real model) ---
    # Winner
    winner = random.choice(["Home", "Away"])
    win_prob = round(random.uniform(0.55, 0.85), 3)

    # Over/Under
    line = game.get("market_line") or round(random.uniform(180, 240), 1)
    ou = random.choice(["Over", "Under"])
    p_over = round(random.uniform(0.51, 0.78), 3)
    over_odds = round(random.uniform(1.80, 2.10), 2)
    under_odds = round(random.uniform(1.80, 2.10), 2)

    # Edge (Kelly-style)
    if ou == "Over":
        edge = (p_over * over_odds - 1) / over_odds
    else:
        edge = ((1 - p_over) * under_odds - 1) / under_odds
    edge = max(round(edge, 3), 0.0)

    # Confidence (composite)
    confidence = round(0.7 * win_prob + 0.3 * p_over, 3) * 100  # %

    # Reasons
    reasons = [
        f"Form: {home} 3W-2L" if winner == "Home" else f"Form: {away} 4W-1L",
        f"H2H: Last 5 → {random.choice(['3-2', '4-1', '2-3'])}",
        f"Pace: High ({random.randint(95, 105)})",
        "No major injuries"
    ]

    return {
        "predicted_winner": winner,
        "win_prob": win_prob,
        "ou_prediction": ou,
        "market_line": line,
        "p_over_percent": f"{int(p_over*100)}%",
        "over_odds": over_odds,
        "under_odds": under_odds,
        "edge": edge,
        "reasons": reasons,
        "composite_score": confidence,
        "model_version": "v0.1 (mock)"
    }
