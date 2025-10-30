# modules/api_handler.py — FINAL: ALL OFFICIAL LEAGUES + MOCK FALLBACK
import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime

# === CONFIG ===
with open("config.json") as f:
    cfg = json.load(f)

API_BASE = cfg["API_BASE_URL"]
API_KEY = cfg["API_KEY"]
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": cfg["HOST"]
}

# === ALL OFFICIAL LEAGUE IDs (RapidAPI Basketball) ===
LEAGUE_IDS = {
    "NBA": "12",
    "EuroLeague": "132",
    "NCAA": "108",
    "WNBA": "111",
    "CBA": "116",
    "KBL": "117",
    "ACB": "118",
    "BSL": "119",
    "LNB": "120",
    "VTB": "121",
    "BCL": "122",
    "NBL": "123",
    "LKL": "124",
    "LNB Pro B": "125",
    "NBL1": "126",
    "PBA": "127",
    "ABL": "128",
    "LNA": "129",
    "LNB Pro A": "130",
    "LNB Pro B": "131"
}

# === MOCK GAMES (FALLBACK) ===
def mock_games(date_str):
    return pd.DataFrame([
        {
            "id": "mock_nba_1",
            "date": f"{date_str}T20:00:00.000Z",
            "teams": {"home": {"name": "Lakers"}, "away": {"name": "Warriors"}},
            "league": {"name": "NBA"}
        },
        {
            "id": "mock_euro_1",
            "date": f"{date_str}T19:30:00.000Z",
            "teams": {"home": {"name": "Real Madrid"}, "away": {"name": "Barcelona"}},
            "league": {"name": "EuroLeague"}
        },
        {
            "id": "mock_ncaa_1",
            "date": f"{date_str}T21:00:00.000Z",
            "teams": {"home": {"name": "Duke"}, "away": {"name": "UNC"}},
            "league": {"name": "NCAA"}
        }
    ])

# === FETCH ALL LEAGUES ===
@st.cache_data(ttl=1800)  # 30 min cache
def get_games(date_str):
    all_games = []
    
    for name, league_id in LEAGUE_IDS.items():
        url = f"{API_BASE}/games"
        params = {
            "date": date_str,
            "league": league_id,
            "season": "2024"  # Adjust per league if needed
        }
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=8)
            if response.status_code == 200:
                data = response.json().get("response", [])
                for game in data:
                    if game.get("status", {}).get("long") in ["Not Started", "Postponed"]:
                        game["league"]["name"] = name  # Override with readable name
                        all_games.append(game)
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            continue

    if all_games:
        df = pd.DataFrame(all_games)
        df = df.sort_values("date")
        return df
    else:
        st.warning("No live games. Using mock data.")
        return mock_games(date_str)

# === ODDS (MOCK FOR NOW) ===
def get_stake_odds(game_id):
    if "mock" in game_id:
        return {
            "market_line": 215.5,
            "over_odds": 1.91,
            "under_odds": 1.89
        }
    return {}
