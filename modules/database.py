# modules/database.py — REPLACED: In-memory storage (no SQLite)
import streamlit as st

def init_db():
    if "predictions" not in st.session_state:
        st.session_state.predictions = []

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
        "p_over_percent": float(pred.get("p_over_percent", 0.0)),
        "over_odds": float(pred.get("over_odds", 0.0)),
        "under_odds": float(pred.get("under_odds", 0.0)),
        "edge": float(pred.get("edge", 0.0)),
        "reasons": " | ".join([str(r) for r in pred.get("reasons", [])])
    }
    st.session_state.predictions.append(data)

def get_best_choices(threshold=0.7, edge_min=0.05):
    init_db()
    df = pd.DataFrame(st.session_state.predictions)
    if df.empty:
        return df
    filtered = df[
        (df["win_prob"] >= threshold) &
        (df["edge"] >= edge_min)
    ].sort_values(by=["edge", "win_prob"], ascending=[False, False]).head(20)
    return filtered
