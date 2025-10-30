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
    # === GLOWING HOOPAI + 15 BOUNCING BASKETBALLS ===
    st.markdown("""
    <div style="text-align:center; padding:40px 0; position:relative; overflow:hidden;">
        <h1 style="font-size:5rem; font-weight:900; color:#00d4aa;
                   text-shadow: 0 0 20px #00d4aa, 0 0 40px #00d4aa;
                   animation: glow 2s infinite alternate; margin:0;">
            HOOPAI
        </h1>
        <p style="color:#aaa; font-size:1.2rem; margin:10px 0 30px;">
            Private Beta • Your Edge Engine
        </p>

        <!-- 15 BOUNCING BASKETBALLS -->
        <div style="height:80px; position:relative;">
            <span style="position:absolute; left:3%;  animation: bounce 1.5s infinite; animation-delay:0s;   font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:7%;  animation: bounce 1.5s infinite; animation-delay:0.1s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:11%; animation: bounce 1.5s infinite; animation-delay:0.2s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:15%; animation: bounce 1.5s infinite; animation-delay:0.3s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:19%; animation: bounce 1.5s infinite; animation-delay:0.4s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:23%; animation: bounce 1.5s infinite; animation-delay:0.5s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:27%; animation: bounce 1.5s infinite; animation-delay:0.6s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:31%; animation: bounce 1.5s infinite; animation-delay:0.7s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:35%; animation: bounce 1.5s infinite; animation-delay:0.8s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:39%; animation: bounce 1.5s infinite; animation-delay:0.9s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:43%; animation: bounce 1.5s infinite; animation-delay:1.0s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:47%; animation: bounce 1.5s infinite; animation-delay:1.1s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:51%; animation: bounce 1.5s infinite; animation-delay:1.2s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:55%; animation: bounce 1.5s infinite; animation-delay:1.3s; font-size:2.5rem;">🏀</span>
            <span style="position:absolute; left:59%; animation: bounce 1.5s infinite; animation-delay:1.4s; font-size:2.5rem;">🏀</span>
        </div>
    </div>

    <style>
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-25px); }
    }
    @keyframes glow {
        from { text-shadow: 0 0 20px #00d4aa, 0 0 40px #00d4aa; }
        to { text-shadow: 0 0 30px #00d4aa, 0 0 60px #00d4aa; }
    }
    </style>
    """, unsafe_allow_html=True)

    # === LOGIN FORM ===
    col1, col2 = st.columns([1, 1])
    with col1:
        email = st.text_input("Email", value="admin@hoopai.com", disabled=True)
        pwd = st.text_input("Password", type="password", placeholder="Enter password")
        if st.button("LOGIN", type="primary", use_container_width=True):
            if _check(email, pwd):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid password")
    with col2:
        st.info("**Only You Can Access**\n\n- Beta locked\n- No new signups")

def require_auth():
    init()
    if not st.session_state.get("authenticated"):
        login()
        st.stop()
