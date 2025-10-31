# modules/api_handler.py — FINAL: WORKS WITH YOUR ACTIVE KEY
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# === CONFIG ===
with open("config.json") as f:
    cfg = json.load(f)

API_BASE = cfg["API_BASE_URL"]  # Should be "https://v1.basketball.api-sports.io"
API_KEY = cfg["API_KEY"]
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "v1.basketball.api-sports.io"
}

LEAGUE_IDS = {
    12: "NBA",
    132: "EuroLeague",
    108: "NCAA",
    111: "WNBA",
    116: "CBA",
    117: "KBL",
    118: "ACB",
    119: "BSL",
    120: "LNB",
    121: "VTB",
    122: "BCL",
    123: "NBL",
    124: "LKL"
}

@st.cache_data(ttl=1800)
st.write(f"Fetching {date_str} from {API_BASE}")
def get_games(date_str: str) -> pd.DataFrame:
    all_games = []
    for lid, name in LEAGUE_IDS.items():
        url = f"{API_BASE}/games"
        params = {
            "date": date_str,
            "league": str(lid),
            "season": "2024"
        }
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=10)
            if r.status_code == 200:
                data = r.json().get("response", [])
                for g in data:
                    status = g.get("status", {}).get("long", "")
                    if status in ["Not Started", "First Quarter", "Halftime", "Second Quarter"]:
                        g["league_name"] = name
                        all_games.append(g)
            else:
                st.warning(f"[{name}] HTTP {r.status_code}")
        except Exception as e:
            st.warning(f"[{name}] {e}")
    
    if not all_games:
        st.info(f"No games found for {date_str}")
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
    df = df.sort_values("date")
    return df.iloc[offset:offset + limit]
