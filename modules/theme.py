import streamlit as st

def apply():
    theme = st.session_state.get("theme", "dark")
    if theme == "light":
        st.markdown("""
        <style>
            .main {background: #f8f9fa; color: #212529;}
            .card {background: white; color: #212529; box-shadow: 0 4px 12px rgba(0,0,0,0.1);}
            .stButton>button {background: #007bff; color: white; border-radius: 12px;}
            h1, h2, h3 {color: #007bff !important;}
            .chip {padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85em;}
            .win {background: #28a745; color: white;}
            .loss {background: #dc3545; color: white;}
            .value {background: #007bff; color: white;}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .main {background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white;}
            .card {background: #1a1a2e; color: white; box-shadow: 0 6px 20px rgba(0,212,170,0.25); border-radius: 18px;}
            .stButton>button {background: #00d4aa; color: black; font-weight: bold; border-radius: 12px;}
            h1, h2, h3 {color: #00d4aa !important;}
            .chip {padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85em;}
            .win {background: #28a745; color: white;}
            .loss {background: #dc3545; color: white;}
            .value {background: #00d4aa; color: black;}
            .icon-btn {background: none; border: none; font-size: 1.6em; cursor: pointer;}
        </style>
        """, unsafe_allow_html=True)
