import streamlit as st
import hashlib
import json
import os

USER_DB = "data/users.json"

# === ANIMATED BASKETBALL CSS ===
ANIM_CSS = """
<style>
/* Animated Basketball */
.basketball {
    width: 50px; height: 50px;
    background: radial-gradient(circle at 30% 30%, #ff8c00, #e65c00);
    border-radius: 50%;
    position: absolute;
    animation: bounce 2s infinite ease-in-out;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
.basketball::after {
    content: '';
    position: absolute;
    top: 15px; left: 15px;
    width: 20px; height: 20px;
    background: #fff;
    border-radius: 50%;
    opacity: 0.7;
}
@keyframes bounce {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-30px) rotate(180deg); }
}
@keyframes fly {
    0% { transform: translateX(-100vw) translateY(-50px) rotate(0deg); }
    100% { transform: translateX(100vw) translateY(50px) rotate(720deg); }
}
.hoop {
    width: 80px; height: 60px;
    border: 8px solid #fff;
    border-top: none;
    border-radius: 0 0 40px 40px;
    position: absolute;
    bottom: 20px; right: 10%;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
.net {
    width: 100px; height: 80px;
    background: repeating-linear-gradient(0deg, #fff, #fff 5px, transparent 5px, transparent 10px);
    position: absolute;
    bottom: -20px; right: 0;
    opacity: 0.8;
}
</style>
"""

# === BETA LOCK: ONLY YOU CAN ACCESS ===
def init():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(USER_DB):
        # ONLY YOU CAN EVER SIGN UP
        default = {"admin@hoopai.com": hashlib.sha256("hoopai123".encode()).hexdigest()}
        with open(USER_DB, "w") as f:
            json.dump(default, f)

def hash_pwd(p): return hashlib.sha256(p.encode()).hexdigest()

def _check(email, pwd):
    if not os.path.exists(USER_DB): return False
    with open(USER_DB) as f: users = json.load(f)
    return users.get(email) == hash_pwd(pwd)

def _save(email, pwd):
    # BETA: ONLY ALLOW YOUR EMAIL
    if email != "admin@hoopai.com":
        return False
    with open(USER_DB, "w") as f:
        json.dump({email: hash_pwd(pwd)}, f)
    return True

def login():
    st.markdown(ANIM_CSS, unsafe_allow_html=True)
    
    # === ANIMATED HEADER ===
    st.markdown("""
    <div style="text-align:center; padding:40px 0; position:relative; overflow:hidden; height:300px;">
        <h1 style="font-size:4rem; font-weight:900; color:#00d4aa;
                   text-shadow: 0 0 20px rgba(0,212,170,0.5);
                   animation: glow 2s infinite alternate;">
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

    # === LOGIN FORM ===
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
        st.caption("Contact: admin@hoopai.com")

def require_auth():
    init()
    if not st.session_state.get("authenticated"):
        login()
        st.stop()
