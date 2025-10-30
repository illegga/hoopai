# modules/ui_components.py — FINAL: Safe access + fallback
import streamlit as st

def prediction_card(game, pred, show_add=False):
    # === SAFE ACCESS ===
    try:
        home = game['teams']['home']['name']
        away = game['teams']['away']['name']
    except:
        home = "Home Team"
        away = "Away Team"

    try:
        date = game['date'][:10]
    except:
        date = "Unknown"

    # === CARD ===
    with st.container():
        st.markdown(f"""
        <div style="background:#1a1a2e; padding:15px; border-radius:12px; margin:10px 0; border-left:4px solid #00d4aa;">
            <h4 style="margin:0; color:#00d4aa;">{home} vs {away}</h4>
            <p style="margin:5px 0; color:#aaa; font-size:0.9rem;">{date} • {pred['model_version']}</p>
            <div style="display:flex; justify-content:space-between; margin:10px 0;">
                <span><strong>Winner:</strong> {pred['predicted_winner']} ({int(pred['win_prob']*100)}%)</span>
                <span><strong>{pred['ou_prediction']} {pred['market_line']}</strong> @ {pred['over_odds'] if pred['ou_prediction']=='Over' else pred['under_odds']}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.9rem;">
                <span>Edge: <strong>{pred['edge']:+.1%}</strong></span>
                <span>Confidence: <strong>{pred['composite_score']:.2f}</strong></span>
            </div>
            <details style="margin-top:10px;">
                <summary style="cursor:pointer; color:#00d4aa;">Reasons</summary>
                <ul style="margin:5px 0; padding-left:20px;">
                    {"".join(f"<li>{r}</li>" for r in pred.get('reasons', ['No data']))}
                </ul>
            </details>
        </div>
        """, unsafe_allow_html=True)

        if show_add:
            col1, col2 = st.columns([3, 1])
            with col1:
                stake = st.number_input(
                    "Stake (₦)", min_value=1000, value=5000, step=1000,
                    key=f"stake_{game.get('id', 'unknown')}"
                )
            with col2:
                if st.button("Add", key=f"add_{game.get('id', 'unknown')}"):
                    potential = stake * (pred['over_odds'] if pred['ou_prediction']=='Over' else pred['under_odds'])
                    st.session_state.slip.append({
                        'match': f"{home} vs {away}",
                        'pick': f"{pred['ou_prediction']} {pred['market_line']}",
                        'odds': pred['over_odds'] if pred['ou_prediction']=='Over' else pred['under_odds'],
                        'stake': stake,
                        'potential': round(potential)
                    })
                    st.success("Added to slip!")
