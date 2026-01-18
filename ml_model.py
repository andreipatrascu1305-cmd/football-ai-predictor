import joblib
import os
import pandas as pd
import numpy as np
from online_data import get_online_elo

MODEL_H_PATH = "model_home_goals.pkl"
MODEL_A_PATH = "model_away_goals.pkl"

def get_prediction_by_name(home_team_name, away_team_name):
    # 1. Scraping
    home_rank = get_online_elo(home_team_name)
    away_rank = get_online_elo(away_team_name)

    if home_rank is None: return f"⚠️ Nu am găsit '{home_team_name}'."
    if away_rank is None: return f"⚠️ Nu am găsit '{away_team_name}'."

    # 2. Verificare Modele
    if not os.path.exists(MODEL_H_PATH) or not os.path.exists(MODEL_A_PATH):
        return "Eroare: Modelele nu sunt antrenate!"

    # 3. Predicție Goluri
    model_h = joblib.load(MODEL_H_PATH)
    model_a = joblib.load(MODEL_A_PATH)
    
    input_data = pd.DataFrame([[home_rank, away_rank]], columns=['home_rank', 'away_rank'])
    
    goals_h = model_h.predict(input_data)[0]
    goals_a = model_a.predict(input_data)[0]

    score_h = int(round(goals_h))
    score_a = int(round(goals_a))

    # --- CALCUL 1: PROBABILITATEA DE VICTORIE (Textul) ---
    # Aceasta rămâne bazată pe goluri
    total_goals = goals_h + goals_a + 0.01
    win_prob_h = int((goals_h / total_goals) * 100)
    win_prob_a = int((goals_a / total_goals) * 100)

    # --- CALCUL 2: ÎNCREDEREA AI-ULUI (Bara) ---
    # Aceasta se bazează pe diferența de valoare (Rank)
    # Dacă diferența e mare, AI-ul e sigur. Dacă e mică, e confuz.
    
    rank_diff = abs(home_rank - away_rank)
    
    # Formula Secretă: Plecăm de la 50% și adăugăm puncte pentru diferența de valoare
    # La fiecare 5 locuri diferență în clasament, adăugăm 1% încredere
    ai_confidence = 55 + (rank_diff / 4)
    
    # Bonus: Dacă diferența de goluri prezisă e mare (>1.5), creștem încrederea
    goal_diff = abs(goals_h - goals_a)
    if goal_diff > 1.5:
        ai_confidence += 15
        
    # Nu lăsăm să treacă de 98% (nimic nu e perfect) sau să scadă sub 40%
    ai_confidence = min(98, max(40, int(ai_confidence)))

    # --- GENERARE MESAJ ---
    diff = abs(goals_h - goals_a)
    msg_prob = ""

    if diff < 0.35:
        msg_prob = f"Șanse de EGAL: {max(win_prob_h, win_prob_a)}% (Meci Strâns)"
    elif goals_h > goals_a:
        msg_prob = f"Șanse victorie {home_team_name}: {win_prob_h}%"
    else:
        msg_prob = f"Șanse victorie {away_team_name}: {win_prob_a}%"

    return {
        "score": f"{score_h} - {score_a}",
        "details": f"Rank UEFA: {home_rank} vs {away_rank}",
        "probability": msg_prob,       # Textul (ex: 60%)
        "prob_value": ai_confidence,   # Bara (ex: 85% sigur)
        "raw_goals": f"(Estimat AI: {goals_h:.2f} vs {goals_a:.2f} goluri)"
    }