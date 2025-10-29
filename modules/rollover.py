import pandas as pd
from modules.database import get_prediction

def generate_daily_rollover(date_str, target_odds, threshold=0.70, max_games=5):
    from modules.database import get_finished_games
    games = get_finished_games(date_str)
    candidates = []
    for _, g in games.iterrows():
        p = get_prediction(g['id'])
        if not p or p['win_prob'] < threshold: continue
        odds = p['over_odds'] if p['ou_prediction']=='Over' else p['under_odds']
        candidates.append({
            'game': g, 'pred': p, 'odds': odds, 'prob': p['win_prob']
        })
    candidates.sort(key=lambda x: x['prob'], reverse=True)
    
    selected = []
    current = 1.0
    for c in candidates[:max_games]:
        next_odds = current * c['odds']
        if next_odds >= target_odds: break
        selected.append(c)
        current = next_odds
    
    if len(selected) < 2: return None
    return {
        'target': target_odds,
        'games': selected,
        'combined_odds': round(current, 2),
        'date': date_str
    }
