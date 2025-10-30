# modules/auth.py — FINAL: GLOWING HOOPAI + 15 BOUNCING BASKETBALLS ON LOGIN
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
    with open(USER_DB) as f: users = json.dump(f)
    return users.get(email) == hash_pwd(pwd)

def login():
    # === FULL ANIMATED LOGIN SCREEN ===
    st.markdown("""
    <div style="text-align:center; padding:60px 20px; background:linear-gradient(135deg, #0f0c29, #302b63); border-radius:24px; margin:20px; box-shadow:0 15px 40px rgba(0,212,170,0.4);">
        <!-- GLOWING HOOPAI -->
        <h1 style="font-size:6.5rem; font-weight:900; color:#00d4aa;
                   text-shadow: 0 0 25px #00d4aa, 0 0 50px #00d4aa, 0 0 75px #00d4aa, 0 0 100px #00d4aa;
                   animation: glow 2s infinite alternate; margin:15px 0;">
            HOOPAI
        </h1>
        <p style="color:#ccc; font-size:1.5rem; margin:15px 0 50px; font-weight:300;">
            Private Beta • Your Edge Engine
        </p>

        <!-- 15 BOUNCING BASKETBALLS -->
        <div style="height:140px; position:relative; margin:40px 0;">
            <span style="position:absolute; left:0%;   animation: bounce 1.5s infinite; animation-delay:0s;   font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:4%;   animation: bounce 1.5s infinite; animation-delay:0.1s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:8%;   animation: bounce 1.5s infinite; animation-delay:0.2s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:12%;  animation: bounce 1.5s infinite; animation-delay:0.3s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:16%;  animation: bounce 1.5s infinite; animation-delay:0.4s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:20%;  animation: bounce 1.5s infinite; animation-delay:0.5s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:24%;  animation: bounce 1.5s infinite; animation-delay:0.6s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:28%;  animation: bounce 1.5s infinite; animation-delay:0.7s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:32%;  animation: bounce 1.5s infinite; animation-delay:0.8s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:36%;  animation: bounce 1.5s infinite; animation-delay:0.9s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:40%;  animation: bounce 1.5s infinite; animation-delay:1.0s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:44%;  animation: bounce 1.5s infinite; animation-delay:1.1s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:48%;  animation: bounce 1.5s infinite; animation-delay:1.2s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:52%;  animation: bounce 1.5s infinite; animation-delay:1.3s; font-size:3.2rem; color:#ff8c00;">🏀</span>
            <span style="position:absolute; left:56%;  animation: bounce 1.5s infinite; animation-delay:1.4s; font-size:3.2rem; color:#ff8c00;">🏀</span>
        </div>
    </div>

    <!-- CSS ANIMATIONS -->
    <style>
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-40px); }
    }
    @keyframes glow {
        from { text-shadow: 0 0 25px #00d4aa, 0 0 50px #00d4aa, 0 0 75px #00d4aa, 0 0 100px #00d4aa; }
        to { text-shadow: 0 0 35px #00d4aa, 0 0 70px #00d4aa, 0 0 100px #00d4aa, 0 0 130px #00d4aa; }
    }
    </style>
    """, unsafe_allow_html=True)

    # === LOGIN FORM ===
    col1, col2 = st.columns([1, 1])
    with col1:
        email = st.text_input("Email", value="admin@hoopai.com", disabled=True)
        pwd = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.button("LOGIN", type="primary", use_container_width=True):
            if _check(email, pwd):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid password")
    with col2:
        st.info("**Only You Can Access**\n\n- Beta locked\n- No new signups\n- Your domain only")

def require_auth():
    init()
    if not st.session_state.get("authenticated"):
        login()
        st.stop()
