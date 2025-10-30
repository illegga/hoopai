# app.py  (only the changed parts – replace the old Predictions tab & header)

import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# -------------------------------------------------
# IMPORTS (keep your existing ones)
# -------------------------------------------------
from modules.api_handler import (
    get_all_upcoming_games, paginate, get_live_scores, get_stake_odds
)
from modules.predictor import predict_game
from modules.ui_components import prediction_card
# ... your other imports ...

# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = 1
if "start_date" not in st.session_state:
    st.session_state.start_date = datetime.now(pytz.timezone("Africa/Lagos")).date()
if "days_ahead" not in st.session_state:
    st.session_state.days_ahead = 7

# -------------------------------------------------
# HEADER (Live-Score button stays here)
# -------------------------------------------------
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.header("HOOPAI")
with col2:
    st.selectbox("Theme", ["dark", "light"], key="theme", on_change=apply)
with col3:
    if st.button("Live Scores", key="live_btn"):
        lives = get_live_scores()
        if lives:
            st.subheader("Live Games")
            for g in lives:
                home = g["teams"]["home"]["name"]
                away = g["teams"]["away"]["name"]
                hs = g["scores"]["home"]["total"]
                as_ = g["scores"]["away"]["total"]
                st.write(f"**{home} {hs} – {as_} {away}**")
                st.caption(f"{g['league']['name']} | {g['period']} | {g['time']}")
        else:
            st.info("No live games right now.")

# -------------------------------------------------
# PREDICTIONS TAB (50 per page, pagination, multi-date)
# -------------------------------------------------
with tab1:
    st.header("Predictions")

    # ----- DATE & RANGE -----
    c1, c2 = st.columns([2, 1])
    with c1:
        start_date = st.date_input(
            "Start Date", st.session_state.start_date,
            key="start_date_input"
        )
    with c2:
        days_ahead = st.selectbox(
            "Days Ahead", [1, 3, 7, 14, 30],
            index=[1, 3, 7, 14, 30].index(st.session_state.days_ahead),
            key="days_ahead_input"
        )

    # ----- FETCH ALL GAMES -----
    games_df = get_all_upcoming_games(str(start_date), days_ahead)

    if games_df.empty:
        st.error("No upcoming games – check API key or date range.")
    else:
        st.info(f"Found **{len(games_df)}** upcoming games across {len(LEAGUE_IDS)} leagues.")

        # ----- PAGINATION -----
        per_page = 50
        total_pages = (len(games_df) + per_page - 1) // per_page
        page = st.selectbox(
            "Page", range(1, total_pages + 1),
            index=st.session_state.page - 1,
            key="page_select"
        )
        st.session_state.page = page

        page_df = paginate(games_df, page, per_page)

        for _, row in page_df.iterrows():
            pred = predict_game(row.to_dict())
            prediction_card(row, pred)

        # ----- NEXT BUTTON -----
        if page < total_pages:
            if st.button("Next Page", key="next_page_btn"):
                st.session_state.page = page + 1
                st.experimental_rerun()
