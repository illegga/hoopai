import requests, pandas as pd, streamlit as st
import json

with open("config.json") as f: cfg = json.load(f)
HEADERS = {"x-rapidapi-key": cfg["API_KEY"], "x-rapidapi-host": cfg["HOST"]}
BASE = cfg["API_BASE_URL"]

@st.cache_data(ttl=600)
def get_games(date_str):
    r = requests.get(f"{BASE}/games", headers=HEADERS, params={"date": date_str})
    return pd.json_normalize(r.json().get("response", []))

@st.cache_data(ttl=300)
def get_stake_odds(gid):
    r = requests.get(f"{BASE}/odds", headers=HEADERS, params={"game": gid})
    data = r.json().get("response", [])
    if not data: return {}
    for book in data[0]["bookmakers"]:
        if "stake" in book["name"].lower():
            for bet in book["bets"]:
                if "total" in bet["name"].lower():
                    o = bet["values"][0]; u = bet["values"][1]
                    return {"market_line": float(o["value"]), "over_odds": float(o["odd"]), "under_odds": float(u["odd"])}
    return {}
