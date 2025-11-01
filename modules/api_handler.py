import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta

# === CONFIG ===
with open("config.json") as f:
    cfg = json.load(f)

API_BASE = cfg["API_BASE_URL"]
API_KEY = cfg["API_KEY"]
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": cfg["HOST"]
}

LEAGUE_IDS = {
    12: "NBA", 132: "EuroLeague", 108: "NCAA", 111: "WNBA",
    116: "CBA", 117: "KBL", 118: "ACB", 119: "BSL",
    120: "LNB", 121: "VTB", 122: "BCL", 123: "NBL",
    124: "LKL"
}

@st.cache_data(ttl=1800)
def get_games(date_str: str) -> pd.DataFrame:
    print(f"Fetching {date_str}")
    all_games = []
    for lid, name in LEAGUE_IDS.items():
        url = f"{API_BASE}/games"
        params = {"date": date_str, "league": str(lid), "season": "2024"}
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=10)
            if r.status_code == 200:
                for g in r.json().get("response", []):
                    status = g.get("status", {}).get("long", "")
                    if status in ["Not Started", "First Quarter", "Halftime"]:
                        g["league_name"] = name
                        all_games.append(g)
        except Exception as e:
            print(f"Error {name}: {e}")
    if not all_games:
        return pd.DataFrame()
    df = pd.DataFrame(all_games)
    df["time_local"] = pd.to_datetime(df["date"]).dt.tz_convert("Africa/Lagos").dt.strftime("%H:%M WAT")
    return df.sort_values("date")

@st.cache_data(ttl=1800)
def get_upcoming_matches(limit: int = 100, offset: int = 0) -> pd.DataFrame:
    all_games = []
    today = datetime.utcnow().date()
    for i in range(7):
        d = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        df_day = get_games(d)
        if not df_day.empty:
            all_games.append(df_day)
    if not all_games:
        return pd.DataFrame()
    df = pd.concat(all_games, ignore_index=True)
    return df.sort_values("date").iloc[offset:offset + limit]

@st.cache_data(ttl=600)
def get_live_scores() -> list:
    url = f"{API_BASE}/games"
    params = {"status": "Live"}
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=5)
        if r.status_code == 200:
            return r.json().get("response", [])
    except:
        pass
    return []
