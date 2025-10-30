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
    st.markdown('<div class="login-form">', unsafe_allow_html=True)
    st.markdown("### Login to HoopAI")
    col1, col2 = st.columns([1, 1])
    with col1:
        email = st.text_input("Email", value="admin@hoopai.com", disabled=True)
        pwd = st.text_input("Password", type="password")
        if st.button("LOGIN", type="primary", use_container_width=True):
            if _check(email, pwd):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Wrong password")
    with col2:
        st.info("**Beta Access Only**")
    st.markdown('</div>', unsafe_allow_html=True)

def require_auth():
    init()
    if not st.session_state.get("authenticated"):
        login()
        st.stop()
