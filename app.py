# app.py — FINAL: GLOWING HOOPAI BEFORE & AFTER LOGIN
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# === PAGE CONFIG (MUST BE FIRST) ===
st.set_page_config(page_title="HoopAI", layout="wide", page_icon="basketball")

# === IMPORTS ===
from modules.auth import require_auth
from modules.theme import apply
from modules.stake_sim import init, place
from modules.api_handler import get_games
from modules.predictor import predict_game
from modules.ui_components import prediction_card
from modules.database import get_best_choices
from modules.rollover import generate_daily_rollover

# === AUTH & INIT ===
require_auth()
init()
apply()

# === TIMEZONE ===
WAT = pytz.timezone('Africa/Lagos')

# === GLOWING HOOPAI HEADER (AFTER LOGIN) ===
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.markdown("""
    <h1 style="text-align:center; font-size:5rem; font-weight:900; color:#00d4aa;
               text-shadow: 0 0 25px #00d4aa, 0 0 50px #00d4aa, 0 0 75px #00d4aa, 0 0 100px #00d4aa;
               animation: glow 2s infinite alternate; margin:20px 0;">
        HOOPAI
    </h1>
    <style>
    @keyframes glow {
        from { text-shadow: 0 0 25px #00d4aa, 0 0 50px #00d4aa, 0 0 75px #00d4aa, 0 0 100px #00d4aa; }
        to { text-shadow: 0 0 35px #00d4aa, 0 0 70px #00d4aa, 0 0 100px #00d4aa, 0 0 130px #00d4aa; }
    }
    </style>
    """, unsafe_allow_html=True)
with col2:
    st.selectbox("Theme", ["dark", "light"], key="theme", on_change=apply)
with col3:
    st.session_state.best_threshold = st.slider("Best Choices Threshold", 0.60, 0.90, 0.70, 0.01, key="thresh")

# === TABS ===
tab1, tab2, tab3, tab4 = st.tabs(["Predictions", "Sim Bets", "Best Choices", "Rollover"])

with tab1:
    st.header("Today's Predictions")
    date = st.date_input("Select Date", datetime.now(WAT).date(), key="pred_date")
    games = get_games(str(date))
    for _, g in games.iterrows():
        pred = predict_game(g)
        prediction_card(g, pred)

with tab2:
    st.header("Sim Bet Slip")
    slip = st.session_state.get("slip", [])
    if slip:
        total = sum(b['stake'] for b in slip)
        pot = sum(b['potential'] for b in slip)
        st.metric("Total Stake", f"₦{total:,.0f}")
        st.metric("Potential Win", f"₦{pot:,.0f}")
        if st.button("PLACE SIM BETS", type="primary", use_container_width=True):
            ok, msg = place()
            st.success(msg) if ok else st.error(msg)
        st.divider()
        for b in slip:
            st.write(f"**{b['match']}** → {b['pick']} @ {b['odds']} → ₦{b['potential']:,.0f}")
    else:
        st.info("Your bet slip is empty. Add games from Predictions.")

with tab3:
    st.header(f"Best Choices (≥ {int(st.session_state.best_threshold*100)}%)")
    df = get_best_choices(threshold=st.session_state.best_threshold, edge_min=0.05)
    if df.empty:
        st.info("No picks meet your threshold. Lower it to see more.")
    else:
        for _, r in df.iterrows():
            pred = {k: r[k] for k in ['predicted_winner','win_prob','ou_prediction','market_line','p_over_percent','over_odds','under_odds','edge','reasons']}
            prediction_card(r, pred, show_add=True)

with tab4:
    st.header("Rollover Builder")
    date_ro = st.date_input("Select Date", datetime.now(WAT).date(), key="ro_date")
    thresh = st.session_state.best_threshold
    ro2 = generate_daily_rollover(str(date_ro), 2.0, threshold=thresh)
    ro5 = generate_daily_rollover(str(date_ro), 5.0, threshold=thresh)
    
    subtab1, subtab2 = st.tabs(["2 Odds Rollover", "5 Odds Rollover"])
    
    with subtab1:
        st.subheader("2 Odds Daily Rollover")
        if ro2:
            st.success(f"**Combined Odds: {ro2['combined_odds']:.2f}**")
            for c in ro2['games']:
                g = c['game']; p = c['pred']
                st.write(f"**{g['teams.home.name']} vs {g['teams.away.name']}**")
                st.caption(f"{p['ou_prediction']} {p['market_line']:.1f} @ {c['odds']} — {int(p['win_prob']*100)}% confidence")
        else:
            st.info("Not enough high-confidence games for 2 odds.")
    
    with subtab2:
        st.subheader("5 Odds Daily Rollover")
        if ro5:
            st.success(f"**Combined Odds: {ro5['combined_odds']:.2f}**")
            for c in ro5['games']:
                g = c['game']; p = c['pred']
                st.write(f"**{g['teams.home.name']} vs {g['teams.away.name']}**")
                st.caption(f"{p['ou_prediction']} {p['market_line']:.1f} @ {c['odds']} — {int(p['win_prob']*100)}% confidence")
        else:
            st.info("Not enough high-confidence games for 5 odds.")
