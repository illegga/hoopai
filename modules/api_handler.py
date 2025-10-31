# modules/api_handler.py
import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
with open("config.json") as f:
    cfg = json.load(f)

API_BASE = cfg["API_BASE_URL"]
API_KEY = cfg["API_KEY"]
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": cfg["HOST"]
}

# -------------------------------------------------
# ALL OFFICIAL LEAGUE IDs
# -------------------------------------------------
LEAGUE_IDS = {
    12: "NBA", 132: "EuroLeague", 108: "NCAA", 111: "WNBA",
    116: "CBA", 117: "KBL", 118: "ACB", 119: "BSL",
    120: "LNB", 121: "VTB", 122: "BCL", 123: "NBL",
    124: "LKL", 125: "LNB Pro B", 126: "NBL1", 127: "PBA",
    128: "ABL", 129: "LNA", 130: "LNB Pro A", 131: "LNB Pro B"
}

# -------------------------------------------------
# FETCH GAMES FOR ONE DATE (used by the date-filter)
# -------------------------------------------------
@st.cache_data(ttl=1800)
def get_games(date_str: str) -> pd.DataFrame:
    """Return all *Not Started* games for a single date."""
    all_games = []
    for lid, name in LEAGUE_IDS.items():
        url = f"{API_BASE}/games"
        params = {"date": date_str, "league": lid, "season": "2024", "status": "Not Started"}
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=5)
            if r.status_code == 200:
                for g in r.json().get("response", []):
                    g["league_name"] = name
                    all_games.append(g)
        except Exception as e:
            st.warning(f"[{name} – {date_str}] {e}")
    if not all_games:
        return pd.DataFrame()
    df = pd.DataFrame(all_games)
    df = df.sort_values("date")
    df["time_local"] = pd.to_datetime(df["date"]).dt.tz_convert("Africa/Lagos").dt.strftime("%H:%M WAT")
    return df


# -------------------------------------------------
# FETCH ALL UPCOMING GAMES (multi-date, used when “no filter”)
# -------------------------------------------------
@st.cache_data(ttl=1800)
def get_upcoming_matches(limit: int = 1000, offset: int = 0) -> pd.DataFrame:
    """Return *all* upcoming games (next 30 days) – paginated."""
    all_games = []
    today = datetime.utcnow().date()
    for i in range(30):                     # next 30 days
        d = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        day_df = get_games(d)
        if not day_df.empty:
            all_games.append(day_df)

    if not all_games:
        return pd.DataFrame()
    df = pd.concat(all_games, ignore_index=True)
    df = df.sort_values("date")
    return df.iloc[offset: offset + limit]


# -------------------------------------------------
# PAGINATION helper
# -------------------------------------------------
def paginate(df: pd.DataFrame, page: int = 1, per_page: int = 50) -> pd.DataFrame:
    start = (page - 1) * per_page
    return df.iloc[start:start + per_page]


# -------------------------------------------------
# LIVE SCORES (10-min cache)
# -------------------------------------------------
@st.cache_data(ttl=600)
def get_live_scores() -> list:
    url = f"{API_BASE}/games"
    params = {"status": "Live", "timezone": "Africa/Lagos"}
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=5)
        if r.status_code == 200:
            return r.json().get("response", [])
    except Exception as e:
        st.warning(f"Live scores error: {e}")
    return []


# -------------------------------------------------
# ODDS (fallback if none)
# -------------------------------------------------
def get_stake_odds(game_id: str):
    url = f"{API_BASE}/odds"
    params = {"game": game_id}
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=5)
        if r.status_code == 200:
            data = r.json().get("response", [])
            if data:
                for book in data[0].get("bookmakers", []):
                    for bet in book.get("bets", []):
                        if "total" in bet["name"].lower():
                            over = bet["values"][0]
                            under = bet["values"][1]
                            return {
                                "market_line": float(over["value"]),
                                "over_odds": float(over["odd"]),
                                "under_odds": float(under["odd"])
                            }
    except Exception:
        pass
    return {"market_line": 215.5, "over_odds": 1.91, "under_odds": 1.89}
# === ADD TO END OF modules/api_handler.py ===
@st.cache_data(ttl=1800)
def get_upcoming_matches(limit: int = 1000, offset: int = 0) -> pd.DataFrame:
    """Fetch ALL upcoming games (next 30 days), then paginate."""
    all_games = []
    today = datetime.utcnow().date()

    for i in range(30):
        d = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        day_df = get_games(d)
        if not day_df.empty:
            all_games.append(day_df)

    if not all_games:
        return pd.DataFrame()

    df = pd.concat(all_games, ignore_index=True)
    df = df.sort_values("date")
    return df.iloc[offset: offset + limit]

@st.cache_data(ttl=1800)
def get_upcoming_matches(limit: int = 1000, offset: int = 0) -> pd.DataFrame:
    all_games = []
    today = datetime.utcnow().date()
    for i in range(30):
        d = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        day_df = get_games(d)
        if not day_df.empty:
            all_games.append(day_df)
    if not all_games:
        return pd.DataFrame()
    df = pd.concat(all_games, ignore_index=True)
    df = df.sort_values("date")
    return df.iloc[offset: offset + limit]
