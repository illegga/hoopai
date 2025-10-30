import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# === PAGE CONFIG FIRST ===
st.set_page_config(page_title="HoopAI", layout="wide", page_icon="🏀")

# === SIMPLE CSS (NO UNSAFE HTML) ===
st.markdown("""
<style>
/* Glowing Title */
.glow-title {
    font-size: 4.5rem;
    font-weight: 900;
    text-align: center;
    color: #00d4aa;
    animation: glow 2s infinite alternate;
    margin: 20px 0;
}
@keyframes glow {
    from { text-shadow: 0 0 10px #00d4aa; }
    to { text-shadow: 0 0 30px #00d4aa, 0 0 50px #00d4aa; }
}

/* Bouncing Balls */
.bounce {
    display: inline-block;
    animation: bounce 1.5s infinite;
    font-size: 2.5rem;
    margin: 0 10px;
}
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-15px); }
}
.b1 { animation-delay: 0s; }
.b2 { animation-delay: 0.3s; }
.b3 { animation-delay: 0.6s; }
.b4 { animation-delay: 0.9s; }
.b5 { animation-delay: 1.2s; }

/* Login Box */
.login-box {
    max-width: 400px;
    margin: 30px auto;
    padding: 25px;
    background: #1a1a2e;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,212,170,0.3);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

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

# === MAIN HEADER (AFTER LOGIN) ===
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.markdown('<h1 class="glow-title">HOOPAI</h1>', unsafe_allow_html=True)
with col2:
    st.selectbox("Theme", ["dark", "light"], key="theme", on_change=apply)
with col3:
    st.session_state.best_threshold = st.slider("Best Choices Threshold", 0.60, 0.90, 0.70, 0.01, key="thresh")

# === TABS ===
tab1, tab2, tab3, tab4 = st.tabs(["Predictions", "Sim Bets", "Best Choices", "Rollover"])

# [Keep your existing tab code here — same as before]
