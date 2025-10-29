import streamlit as st
import pandas as pd
import pytz
WAT = pytz.timezone('Africa/Lagos')

ADD_ICON = "Add"

def prediction_card(game, pred, show_add=True):
    dt = pd.to_datetime(game['date']).astimezone(WAT)
    with st.container():
        st.markdown(f"""
        <div style="background: #1a1a2e; padding: 18px; border-radius: 18px; margin: 14px 0;
                    box-shadow: 0 8px 24px rgba(0,212,170,0.25); font-family: -apple-system;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin:0; color:#00d4aa;">{game['teams.home.name']} vs {game['teams.away.name']}</h4>
                    <p style="margin:4px 0; color:#888; font-size:0.9em;">
                        {dt.strftime('%H:%M WAT')} • {game['league.name']}
                    </p>
                </div>
                {f'<div class="icon-btn">{ADD_ICON}</div>' if show_add else ''}
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px;">
                <div>
                    <strong style="color:#aaa;">Winner</strong><br>
                    <span style="font-size:1.4em; color:white;">{pred['predicted_winner']} {int(pred['win_prob']*100)}%</span>
                </div>
                <div>
                    <strong style="color:#aaa;">{pred['ou_prediction']} {pred['market_line']:.1f}</strong><br>
                    <span style="font-size:1.2em; color:#00d4aa;">@ {pred['over_odds'] if pred['ou_prediction']=='Over' else pred['under_odds']}</span>
                    {f'<span class="chip value">VALUE</span>' if pred.get('edge',0)>0.05 else ''}
                </div>
            </div>
            <details style="margin-top:16px; color:#bbb;">
                <summary style="cursor:pointer;">Why this pick?</summary>
                {''.join([f"<p style='margin:6px 0; color:#ccc;'>• {r}</p>" for r in pred['reasons']])}
            </details>
        </div>
        """, unsafe_allow_html=True)

        if game['status'] == 'Finished':
            aw = 'Home' if game['home_score'] > game['away_score'] else 'Away'
            ao = 'Over' if (game['home_score']+game['away_score']) > pred['market_line'] else 'Under'
            c1, c2 = st.columns(2)
            with c1:
                color = "#28a745" if aw == pred['predicted_winner'] else "#dc3545"
                st.markdown(f"<span class='chip {'win' if aw==pred['predicted_winner'] else 'loss'}'>{'WIN' if aw==pred['predicted_winner'] else 'LOSS'}</span>", unsafe_allow_html=True)
            with c2:
                color = "#28a745" if ao == pred['ou_prediction'] else "#dc3545"
                st.markdown(f"<span class='chip {'win' if ao==pred['ou_prediction'] else 'loss'}'>{'WIN' if ao==pred['ou_prediction'] else 'LOSS'}</span>", unsafe_allow_html=True)

        if show_add:
            if st.button(f"{ADD_ICON} Add to Slip", key=f"slip_{game['id']}", use_container_width=True):
                from modules.stake_sim import add_to_slip
                add_to_slip(game, pred, 5000)
                st.success("Added to Sim Bets!")
