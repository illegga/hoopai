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
    # === ANIMATED LOGIN (CSS in app.py) ===
    st.markdown("""
    <div class="login-container">
        <h1 style="font-size:4rem; font-weight:900; color:#00d4aa; animation:glow 2s infinite alternate;">
            HOOPAI
        </h1>
        <p style="font-size:1.2rem; color:#aaa; margin-top:10px;">
            Private Beta • Your Edge Engine
        </p>

        <!-- Flying Basketballs -->
        <div class="basketball" style="top:50px; left:10%; animation-delay:0s;"></div>
        <div class="basketball" style="top:80px; left:20%; animation: fly 4s infinite linear; animation-delay:1s;"></div>
        <div class="basketball" style="top:40px; left:30%; animation-delay:0.5s;"></div>
        <div class="basketball" style="top:100px; left:40%; animation: fly 3.5s infinite linear; animation-delay:2s;"></div>
        <div class="basketball" style="top:60px; left:50%; animation-delay:1.2s;"></div>

        <!-- Hoop & Net -->
        <div class="hoop"></div>
        <div class="net"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Login to Your Private Beta")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        email = st.text_input("Email", value="admin@hoopai.com", disabled=True)
        pwd = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.button("LOGIN", use_container_width=True, type="primary"):
            if _check(email, pwd):
                st.session_state.authenticated = True
                st.session_state.user = email
                st.success("Access Granted")
                st.rerun()
            else:
                st.error("Invalid Password")

    with col2:
        st.info("**Only You Can Access**")
        st.write("- Beta locked")
        st.write("- No new signups")
        st.write("- Your domain only")

def require_auth():
    init()
    if not st.session_state.get("authenticated"):
        login()
        st.stop()
