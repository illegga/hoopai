import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# === 1. PAGE CONFIG (MUST BE FIRST) ===
st.set_page_config(page_title="HoopAI", layout="wide", page_icon="basketball")

# === 2. FULL ANIMATED LOGIN SCREEN (BEFORE ANYTHING) ===
st.markdown("""
<style>
/* ANIMATIONS */
@keyframes glow {
    from { text-shadow: 0 0 10px #00d4aa; }
    to { text-shadow: 0 0 30px #00d4aa, 0 0 50px #00d4aa; }
}
@keyframes bounce {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-30px) rotate(180deg); }
}
@keyframes fly {
    0% { transform: translateX(-100vw) translateY(-50px) rotate(0deg); }
    100% { transform: translateX(100vw) translateY(50px) rotate(720deg); }
}

/* BASKETBALL */
.basketball {
    width: 50px; height: 50px;
    background: radial-gradient(circle at 30% 30%, #ff8c00, #e65c00);
    border-radius: 50%;
    position: absolute;
    animation: bounce 2s infinite ease-in-out;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    z-index: 10;
}
.basketball::after {
    content: ''; position: absolute; top: 15px; left: 15px;
    width: 20px; height: 20px; background: #fff; border-radius: 50%; opacity: 0.7;
}

/* HOOP */
.hoop {
    width: 80px; height: 60px;
    border: 8px solid #fff; border-top: none;
    border-radius: 0 0 40px 40px;
    position: absolute; bottom: 20px; right: 10%;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3); z-index: 11;
}
.net {
    width: 100px; height: 80px;
    background: repeating-linear-gradient(0deg, #fff, #fff 5px, transparent 5px, transparent 10px);
    position: absolute; bottom: -20px; right: 0; opacity: 0.8; z-index: 10;
}

/* CONTAINER */
.login-bg {
    text-align: center; padding: 60px 0; position: relative;
    overflow: hidden; height: 400px;
    background: linear-gradient(135deg, #0f0c29, #302b63);
    border-radius: 20px; margin: 20px;
    box-shadow: 0 10px 30px rgba(0,212,170,0.3);
}
</style>

<!-- ANIMATED LOGIN SCREEN -->
<div class="login-bg">
    <h1 style="font-size:4.5rem; font-weight:900; color:#00d4aa; animation:glow 2s infinite alternate; margin:0;">
        HOOPAI
    </h1>
    <p style="font-size:1.3rem; color:#aaa; margin:10px 0 30px;">
        Private Beta • Your Edge Engine
    </p>

    <!-- Basketballs -->
    <div class="basketball" style="top:60px; left:8%; animation-delay:0s;"></div>
    <div class="basketball" style="top:90px; left:18%; animation: fly 4s infinite linear; animation-delay:1s;"></div>
    <div class="basketball" style="top:50px; left:28%; animation-delay:0.5s;"></div>
    <div class="basketball" style="top:110px; left:38%; animation: fly 3.5s infinite linear; animation-delay:2s;"></div>
    <div class="basketball" style="top:70px; left:48%; animation-delay:1.2s;"></div>

    <!-- Hoop & Net -->
    <div class="hoop"></div>
    <div class="net"></div>
</div>
""", unsafe_allow_html=True)

# === 3. IMPORTS AFTER ANIMATION ===
from modules.auth import require_auth
from modules.theme import apply
from modules.stake_sim import init, place
from modules.api_handler import get_games
from modules.predictor import predict_game
from modules.ui_components import prediction_card
from modules.database import get_best_choices
from modules.rollover import generate_daily_rollover

# === 4. AUTH & INIT ===
require_auth()
init()
apply()

# === 5. TIMEZONE ===
WAT = pytz.timezone('Africa/Lagos')

# === 6. HEADER (AFTER LOGIN) ===
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.markdown("<h1 style='text-align:center; color:#00d4aa; animation:glow 2s infinite alternate;'>HOOPAI</h1>", unsafe_allow_html=True)
with col2:
    st.selectbox("Theme", ["dark", "light"], key="theme", on_change=apply)
with col3:
    st.session_state.best_threshold = st.slider("Best Choices Threshold", 0.60, 0.90, 0.70, 0.01, key="thresh")

# === 7. TABS (YOUR EXISTING CODE) ===
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
