import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# === PAGE CONFIG FIRST ===
st.set_page_config(page_title="HoopAI", layout="wide", page_icon="basketball")

# === FULL ANIMATED LOGIN SCREEN (BEFORE AUTH) ===
st.markdown("""
<style>
/* GLOW + BASKETBALLS + HOOP */
@keyframes glow { from { text-shadow: 0 0 10px #00d4aa; } to { text-shadow: 0 0 30px #00d4aa, 0 0 50px #00d4aa; } }
@keyframes bounce { 0%, 100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-30px) rotate(180deg); } }
@keyframes fly { 0% { transform: translateX(-100vw) translateY(-50px) rotate(0deg); } 100% { transform: translateX(100vw) translateY(50px) rotate(720deg); } }

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
.hoop {
    width: 80px; height: 60px; border: 8px solid #fff; border-top: none;
    border-radius: 0 0 40px 40px; position: absolute; bottom: 20px; right: 10%;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3); z-index: 11;
}
.net {
    width: 100px; height: 80px;
    background: repeating-linear-gradient(0deg, #fff, #fff 5px, transparent 5px, transparent 10px);
    position: absolute; bottom: -20px; right: 0; opacity: 0.8; z-index: 10;
}
.login-bg {
    text-align: center; padding: 60px 0; position: relative; overflow: hidden;
    height: 400px; background: linear-gradient(135deg, #0f0c29, #302b63);
    border-radius: 20px; margin: 20px; box-shadow: 0 10px 30px rgba(0,212,170,0.3);
}
</style>

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

# === IMPORTS AFTER ANIMATION ===
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

# === HEADER (after login) ===
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.markdown("<h1 style='text-align:center; color:#00d4aa; animation:glow 2s infinite alternate;'>HOOPAI</h1>", unsafe_allow_html=True)
with col2:
    st.selectbox("Theme", ["dark", "light"], key="theme", on_change=apply)
with col3:
    st.session_state.best_threshold = st.slider("Best Choices Threshold", 0.60, 0.90, 0.70, 0.01, key="thresh")

# === TABS ===
tab1, tab2, tab3, tab4 = st.tabs(["Predictions", "Sim Bets", "Best Choices", "Rollover"])

# [Rest of your tabs code — SAME AS BEFORE]
# ... (keep your Predictions, Sim Bets, Best Choices, Rollover code here)
