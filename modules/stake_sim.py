import streamlit as st
from datetime import datetime

SLIP = "slip"; BANK = "bank"; LOG = "log"

def init():
    if BANK not in st.session_state:
        with open("config.json") as f: cfg = json.load(f)
        st.session_state[BANK] = cfg["INITIAL_BANKROLL_NGN"]
        st.session_state[SLIP] = []
        st.session_state[LOG] = []

def add_to_slip(game, pred, stake):
    st.session_state[SLIP].append({
        "id": game['id'],
        "match": f"{game['teams.home.name']} vs {game['teams.away.name']}",
        "pick": f"{pred['ou_prediction']} {pred['market_line']}",
        "odds": pred['over_odds'] if pred['ou_prediction']=='Over' else pred['under_odds'],
        "stake": stake,
        "potential": stake * (pred['over_odds'] if pred['ou_prediction']=='Over' else pred['under_odds'])
    })

def place():
    total = sum(b['stake'] for b in st.session_state[SLIP])
    if total > st.session_state[BANK]: return False, "Not enough ₦"
    st.session_state[BANK] -= total
    for b in st.session_state[SLIP]:
        b['placed'] = datetime.now().isoformat()
        b['status'] = 'pending'
        st.session_state[LOG].append(b.copy())
    st.session_state[SLIP].clear()
    return True, f"₦{total:,.0f} placed!"
