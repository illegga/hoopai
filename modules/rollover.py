# modules/rollover.py — FINAL: Fixed ImportError
import random
from modules.api_handler import get_games
from modules.predictor import predict_game

def generate_daily_rollover(date_str, target_odds, threshold=0.7):
    games = get_games(date_str)
    if games.empty:
        return None

    high_conf = []
    for _, g in games.iterrows():
        pred = predict_game(g.to_dict())
        if pred['win_prob'] >= threshold and pred['edge'] >= 0.05:
            odds = pred.get('over_odds') if pred['ou_prediction'] == 'Over' else pred.get('under_odds')
            if odds and odds >= 1.8:
                high_conf.append({
                    'game': g.to_dict(),
                    'pred': pred,
                    'odds': odds
                })

    if len(high_conf) < 2:
        return None

    # Pick top games to hit target
    selected = []
    current = 1.0
    for item in sorted(high_conf, key=lambda x: x['odds'], reverse=True):
        if len(selected) >= 5:
            break
        if current * item['odds'] > target_odds * 1.1:
            continue
        selected.append(item)
        current *= item['odds']

    if abs(current - target_odds) > 0.5:
        return None

    return {
        'combined_odds': round(current, 2),
        'games': selected
    }
