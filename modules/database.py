import sqlite3, pandas as pd, os

DB = "data/hoopai.db"

def init():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY, league_id INTEGER, league_name TEXT,
        home_id INTEGER, home_name TEXT, away_id INTEGER, away_name TEXT,
        date TEXT, status TEXT, home_score INTEGER, away_score INTEGER, total_points INTEGER
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY, match_id INTEGER, model_version TEXT,
        predicted_winner TEXT, win_prob REAL, ou_prediction TEXT,
        market_line REAL, p_over REAL, over_odds REAL, under_odds REAL,
        edge REAL, reasons TEXT, timestamp TEXT, composite_score REAL
    )''')
    conn.commit(); conn.close()

def save_match(m):
    df = pd.DataFrame([m])
    conn = sqlite3.connect(DB)
    df.to_sql('matches', conn, if_exists='append', index=False)
    conn.close()

def save_prediction(p):
    df = pd.DataFrame([p])
    conn = sqlite3.connect(DB)
    df.to_sql('predictions', conn, if_exists='append', index=False)
    conn.close()

def get_prediction(mid, ver="v7"):
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM predictions WHERE match_id=? AND model_version=?", conn, params=(mid, ver))
    conn.close()
    return df.to_dict('records')[0] if not df.empty else {}

def get_best_choices(threshold=0.70, edge_min=0.05):
    conn = sqlite3.connect(DB)
    sql = f"""
        SELECT m.*, p.*
        FROM matches m
        JOIN predictions p ON p.match_id = m.id
        WHERE p.model_version='v7'
          AND p.win_prob >= {threshold}
          AND p.edge >= {edge_min}
        ORDER BY p.composite_score DESC
    """
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

def get_finished_games(date=""):
    conn = sqlite3.connect(DB)
    sql = "SELECT * FROM matches WHERE status='Finished'"
    if date: sql += f" AND date LIKE '{date}%'"
    df = pd.read_sql(sql, conn)
    conn.close()
    return df
