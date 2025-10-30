import numpy as np
import joblib
import pandas as pd
import os
from scipy.stats import norm
from modules.api_handler import get_stake_odds
from modules.database import save_prediction

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)
VER = "v7"

def train():
    from modules.database import get_finished_games
    df = get_finished_games()
    if len(df) < 500:
        return  # Skip training
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    X, yw, yt = [], [], []
    for _, r in df.iterrows():
        past = df[df['date'] < r['date']]
        if len(past) < 50:
            continue
        feats = _feats(r, past)
        X.append(feats)
        yw.append(1 if r['home_score'] > r['away_score'] else 0)
        yt.append(r['total_points'])
    X = np.array(X)
    split = int(0.8 * len(X))
    from xgboost import XGBClassifier, XGBRegressor
    wm = XGBClassifier(n_estimators=200, max_depth=5, random_state=42)
    wm.fit(X[:split], np.array(yw)[:split])
    tm = XGBRegressor(n_estimators=200, max_depth=5, random_state=42)
    tm.fit(X[:split], np.array(yt)[:split])
    sigma = np.std(np.array(yt)[:split] - tm.predict(X[:split]))
    joblib.dump(wm, f"{MODEL_DIR}/win_{VER}.pkl")
    joblib.dump(tm, f"{MODEL_DIR}/total_{VER}.pkl")
    joblib.dump(sigma, f"{MODEL_DIR}/sigma_{VER}.pkl")

def load():
    try:
        return (
            joblib.load(f"{MODEL_DIR}/win_{VER}.pkl"),
            joblib.load(f"{MODEL_DIR}/total_{VER}.pkl"),
            joblib.load(f"{MODEL_DIR}/sigma_{VER}.pkl")
        )
    except:
        return None, None, None

def _feats(game, past):
    # Placeholder features
    return [105, 105, 0.5, 105, 105, 0.5, 215, 3, 3]

def predict_game(game):
    wm, tm, sigma = load()
    if wm is None:
        # Fallback if no model
        return {
            'match_id': game['id'],
            'predicted_winner': 'Home',
            'win_prob': 0.65,
            'ou_prediction': 'Over',
            'market_line': 215.0,
            'p_over_percent': '55%',
            'over_odds': 1.90,
            'under_odds': 1.90,
            'edge': 0.03,
            'reasons': ['No model trained yet'],
            'composite_score': 0.7,
            'model_version': VER
        }
    feats = np.array([_feats(game, pd.DataFrame())])
    wp = wm.predict_proba(feats)[0][1]
    pw = 'Home' if wp >= 0.5 else 'Away'
    win_prob = round(max(wp, 1-wp), 3)
    mu = tm.predict(feats)[0]
    odds = get_stake_odds(game['id'])
    line = odds.get('market_line', mu)
    p_over = 1 - norm.cdf((line - mu) / sigma) if sigma > 0 else 0.5
    ou = 'Over' if p_over >= 0.5 else 'Under'
    edge = (p_over * odds.get('over_odds', 1.9) - 1) if ou == 'Over' else ((1-p_over) * odds.get('under_odds', 1.9) - 1)
    pred = {
        'match_id': game['id'],
        'predicted_winner': pw,
        'win_prob': win_prob,
        'ou_prediction': ou,
        'market_line': line,
        'p_over_percent': f"{int(p_over*100)}%",
        'over_odds': odds.get('over_odds', 1.9),
        'under_odds': odds.get('under_odds', 1.9),
        'edge': round(edge, 3),
        'reasons': [f"Expected total: {mu:.1f}", f"Stake line: {line}"],
        'composite_score': round(0.7*win_prob + 0.3*p_over, 3),
        'model_version': VER,
        'timestamp': pd.Timestamp.now().isoformat()
    }
    from modules.database import save_prediction
    save_prediction(game_data, pred)
    save_prediction(pred)
    return pred
