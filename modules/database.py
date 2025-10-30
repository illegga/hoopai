# modules/database.py — FINAL: SAFE SQL + hoopai.db
import sqlite3
import pandas as pd
import os

DB_PATH = "data/hoopai.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id TEXT,
        date TEXT,
        home_team TEXT,
        away_team TEXT,
        predicted_winner TEXT,
        win_prob REAL,
        ou_prediction TEXT,
        market_line REAL,
        p_over_percent REAL,
        over_odds REAL,
        under_odds REAL,
        edge REAL,
        reasons TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_prediction(game_data, pred):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    data = {
        "game_id": game_data.get("id"),
        "date": str(game_data.get("date", ""))[:10],
        "home_team": game_data.get("teams", {}).get("home", {}).get("name", ""),
        "away_team": game_data.get("teams", {}).get("away", {}).get("name", ""),
        "predicted_winner": pred.get("predicted_winner", ""),
        "win_prob": float(pred.get("win_prob", 0.0)),
        "ou_prediction": pred.get("ou_prediction", ""),
        "market_line": float(pred.get("market_line", 0.0)),
        "p_over_percent": float(pred.get("p_over_percent", 0.0)),
        "over_odds": float(pred.get("over_odds", 0.0)),
        "under_odds": float(pred.get("under_odds", 0.0)),
        "edge": float(pred.get("edge", 0.0)),
        "reasons": " | ".join(pred.get("reasons", []))
    }
    df = pd.DataFrame([data])
    df.to_sql("predictions", conn, if_exists="append", index=False)
    conn.close()

def get_best_choices(threshold=0.7, edge_min=0.05):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    sql = """
    SELECT * FROM predictions
    WHERE win_prob >= ? AND edge >= ?
    ORDER BY edge DESC, win_prob DESC
    LIMIT 20
    """
    try:
        df = pd.read_sql(sql, conn, params=(threshold, edge_min))
    except Exception as e:
        print(f"DB Error: {e}")
        df = pd.DataFrame()
    conn.close()
    return df if not df.empty else pd.DataFrame()
