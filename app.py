# app.py — FINAL: NO ERRORS, NO IMPORT ISSUES
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

st.set_page_config(page_title="HoopAI", layout="wide", page_icon="basketball")

# === IMPORTS ===
from modules.auth import require_auth
from modules.theme import apply
from modules.stake_sim import init, place
from modules.api_handler import get_games
from modules.predictor import predict_game
from modules.ui_components import prediction_card
from modules.database import init_db, save_prediction, get_best_choices
from modules.rollover import generate_daily_rollover

# === INIT ===
if "best_threshold" not in st.session_state:
    st.session_state.best_threshold = 0.70
if "slip" not in st.session_state:
    st.session_state.slip = []

require_auth()
init()
init_db()
apply()

WAT = pytz.timezone('Africa/Lagos')

# === HEADER ===
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.header("HOOPAI")
with col2:
    st.selectbox("Theme", ["dark", "light"], key="theme", on_change=apply)
with col3:
    st.session_state.best_threshold = st.slider("Threshold", 0.60, 0.90, st.session_state.best_threshold, 0.01)

# === TABS ===
tab1, tab2, tab3, tab4 = st.tabs(["Predictions", "Sim Bets", "Best Choices", "Rollover"])

with tab1:
    st.header("Predictions")
    date = st.date_input("Date", datetime.now(WAT).date(), key="pred_date")
    games = get_games(str(date))
    if games.empty:
        st.info("No games.")
    else:
        for _, g in games.iterrows():
            pred = predict_game(g.to_dict())
            prediction_card(g, pred)

with tab2:
    st.header("Sim Bet Slip")
    slip = st.session_state.slip
    if slip:
        total = sum(b['stake'] for b in slip)
        pot = sum(b['potential'] for b in slip)
        st.metric("Stake", f"₦{total:,.0f}")
        st.metric("Win", f"₦{pot:,.0f}")
        if st.button("PLACE", type="primary"):
            ok, msg = place()
            (st.success if ok else st.error)(msg)
        for b in slip:
            st.write(f"**{b['match']}** @ {b['odds']} → ₦{b['potential']:,.0f}")
    else:
        st.info("Empty slip.")

with tab3:
    st.header(f"Best ≥ {int(st.session_state.best_threshold*100)}%")
    df = get_best_choices(st.session_state.best_threshold, 0.05)
    if df.empty:
        st.info("No picks.")
    else:
        for _, r in df.iterrows():
            pred = {k: r[k] for k in ['predicted_winner','win_prob','ou_prediction','market_line','p_over_percent','over_odds','under_odds','edge','reasons']}
            prediction_card(r, pred, show_add=True)

with tab4:
    st.header("Rollover")
    date_ro = st.date_input("Date", datetime.now(WAT).date(), key="ro_date")
    thresh = st.session_state.best_threshold
    ro2 = generate_daily_rollover(str(date_ro), 2.0, threshold=thresh)
    ro5 = generate_daily_rollover(str(date_ro), 5.0, threshold=thresh)
    
    s1, s2 = st.tabs(["2 Odds", "5 Odds"])
    with s1:
        if ro2:
            st.success(f"Odds: {ro2['combined_odds']:.2f}")
            for c in ro2['games']:
                g = c['game']; p = c['pred']
                st.write(f"**{g['teams']['home']['name']} vs {g['teams']['away']['name']}**")
                st.caption(f"{p['ou_prediction']} {p['market_line']} @ {c['odds']}")
        else:
            st.info("Not enough.")
    with s2:
        if ro5:
            st.success(f"Odds: {ro5['combined_odds']:.2f}")
            for c in ro5['games']:
                g = c['game']; p = c['pred']
                st.write(f"**{g['teams']['home']['name']} vs {g['teams']['away']['name']}**")
                st.caption(f"{p['ou_prediction']} {p['market_line']} @ {c['odds']}")
        else:
            st.info("Not enough.")
