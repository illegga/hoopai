# modules/auth.py — FIXED: 15 Balls with CSS Grid + Glow
import streamlit as st
import hashlib
import json
import os

USER_DB = "data/users.json"

def init():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(USER_DB):
        default = {"admin@hoopai.com": hashlib.sha256("hoopai123".encode()).hexdigest()}
        with open(USER_DB, "w") as f:
            json.dump(default, f)

def hash_pwd(p): return hashlib.sha256(p.encode()).hexdigest()

def _check(email, pwd):
    if not os.path.exists(USER_DB): return False
    with open(USER_DB) as f: users = json.load(f)
    return users.get(email) == hash_pwd(pwd)

def login():
    st.markdown("""
    <style>
    /* GLOWING HOOPAI */
    @keyframes glow {
        from { text-shadow: 0 0 20px #00d4aa, 0 0 40px #00d4aa, 0 0 60px #00d4aa; }
        to { text-shadow: 0 0 30px #00d4aa, 0 0 60px #00d4aa, 0 0 80px #00d4aa; }
    }
    .glow-hoopai {
        font-size: 6rem; font-weight: 900; color: #00d4aa;
        text-align: center; animation: glow 2s infinite alternate;
        margin: 20px 0; text-shadow: 0 0 20px #00d4aa;
    }
    
    /* 15 BASKETBALLS WITH CSS GRID (RELIABLE) */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    .ball-grid {
        display: grid; grid-template-columns: repeat(15, 1fr); gap: 5px;
        justify-content: center; align-items: center; height: 60px;
        margin: 30px 0; animation: bounce 1.5s infinite;
    }
    .ball {
        font-size: 2.5rem; color: #ff8c00; animation: bounce 1.5s infinite;
        text-align: center; animation-delay: calc(var(--i) * 0.1s);
    }
    .ball:nth-child(1) { animation-delay: 0s; }
    .ball:nth-child(2) { animation-delay: 0.1s; }
    .ball:nth-child(3) { animation-delay: 0.2s; }
    .ball:nth-child(4) { animation-delay: 0.3s; }
    .ball:nth-child(5) { animation-delay: 0.4s; }
    .ball:nth-child(6) { animation-delay: 0.5s; }
    .ball:nth-child(7) { animation-delay: 0.6s; }
    .ball:nth-child(8) { animation-delay: 0.7s; }
    .ball:nth-child(9) { animation-delay: 0.8s; }
    .ball:nth-child(10) { animation-delay: 0.9s; }
    .ball:nth-child(11) { animation-delay: 1.0s; }
    .ball:nth-child(12) { animation-delay: 1.1s; }
    .ball:nth-child(13) { animation-delay: 1.2s; }
    .ball:nth-child(14) { animation-delay: 1.3s; }
    .ball:nth-child(15) { animation-delay: 1.4s; }
    
    /* LOGIN BOX */
    .login-box {
        max-width: 400px; margin: 0 auto; padding: 25px;
        background: #1a1a2e; border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,212,170,0.3); text-align: center;
    }
    </style>
    
    <!-- GLOWING HOOPAI -->
    <h1 class="glow-hoopai">HOOPAI</h1>
    
    <!-- 15 BASKETBALLS GRID -->
    <div class="ball-grid">
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
        <span class="ball">🏀</span>
    </div>
    
    <!-- SUBTITLE -->
    <p style="text-align:center; color:#aaa; font-size:1.3rem; margin:20px 0;">
        Private Beta • Your Edge Engine
    </p>
    """, unsafe_allow_html=True)

    # === LOGIN FORM ===
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        email = st.text_input("Email", value="admin@hoopai.com", disabled=True)
        pwd = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.button("LOGIN", type="primary", use_container_width=True):
            if _check(email, pwd):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid password")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.info("**Only You Can Access**\n\n- Beta locked\n- No new signups\n- Your domain only")

def require_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.subheader("Login Required")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Replace with your real check
            if email == "admin@hoopai.com" and password == "hoopai2025":
                st.session_state.authenticated = True
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Wrong email or password")
        st.stop()  # ← THIS STOPS THE PAGE HERE UNTIL LOGIN
