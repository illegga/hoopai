# modules/stake_sim.py — FIXED: Uses your config.json keys
import streamlit as st
import json
import os

def init():
    # Load config (it's already in repo)
    if not os.path.exists("config.json"):
        st.error("config.json missing!")
        st.stop()
    
    with open("config.json") as f:
        cfg = json.load(f)
    
    # Initialize session state from config
    if "bankroll" not in st.session_state:
        st.session_state.bankroll = cfg.get("INITIAL_BANKROLL_NGN", 500000.00)
    if "slip" not in st.session_state:
        st.session_state.slip = []
    if "default_stake" not in st.session_state:
        st.session_state.default_stake = cfg.get("DEFAULT_STAKE_NGN", 5000.00)

def place():
    slip = st.session_state.slip
    if not slip:
        return False, "Your slip is empty."
    
    total_stake = sum(b["stake"] for b in slip)
    if total_stake > st.session_state.bankroll:
        return False, f"Insufficient funds. Need ₦{total_stake:,.0f}, have ₦{st.session_state.bankroll:,.0f}"

    # Simulate outcome (for demo)
    import random
    win = random.random() < 0.6  # 60% win rate (fake)
    
    if win:
        winnings = sum(b["potential"] for b in slip)
        profit = winnings - total_stake
        st.session_state.bankroll += profit
        msg = f"**WIN!** +₦{profit:,.0f} → New balance: ₦{st.session_state.bankroll:,.0f}"
    else:
        st.session_state.bankroll -= total_stake
        msg = f"Loss. -₦{total_stake:,.0f} → Balance: ₦{st.session_state.bankroll:,.0f}"
    
    st.session_state.slip = []
    return True, msg
