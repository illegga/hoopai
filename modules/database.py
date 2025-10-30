# modules/database.py — FINAL: Safe in-memory DB
import streamlit as st
import pandas as pd

def init_db():
    if "predictions" not in st.session_state:
        st.session_state.predictions = []  # ← MUST CREATE LIST

def save_prediction(game_data, pred):
    init_db()
    data = {
        "game_id": str(game_data.get("id", "")),
        "date": str(game_data.get("date", ""))[:10],
        "home_team": str(game_data.get("teams", {}).get("home", {}).get("name", "")),
        "away_team": str(game_data.get("teams", {}).get("away", {}).get("name", "")),
        "predicted_winner": str(pred.get("predicted_winner", "")),
        "win_prob": float(pred.get("win_prob", 0.0)),
        "ou_prediction": str(pred.get("ou_prediction", "")),
        "market_line": float(pred.get("market_line", 0.0)),
        "p_over_percent": str(pred.get("p_over_percent", "50%")),
        "over_odds": float(pred.get("over_odds", 1.9)),
        "under_odds": float(pred.get("under_odds", 1.9)),
        "edge": float(pred.get("edge", 0.0)),
        "reasons": " | ".join([str(r) for r in pred.get("reasons", [])])
    }
    st.session_state.predictions.append(data)

def get_best_choices(threshold=0.7, edge_min=0.05):
    init_db()  # ← ENSURE LIST EXISTS
    if not st.session_state.predictions:
        return pd.DataFrame()
    df = pd.DataFrame(st.session_state.predictions)
    filtered = df[
        (df["win_prob"] >= threshold) &
        (df["edge"] >= edge_min)
    ]
    if filtered.empty:
        return pd.DataFrame()
    return filtered.sort_values(["edge", "win_prob"], ascending=[False, False]).head(20)
