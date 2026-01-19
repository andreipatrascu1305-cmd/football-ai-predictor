import joblib
import os
import pandas as pd
import numpy as np
# IMPORTAM SI FUNCTIA NOUA DE NUME:
from online_data import get_online_elo, get_official_name

MODEL_H_PATH = "model_home_goals.pkl"
MODEL_A_PATH = "model_away_goals.pkl"

def get_prediction_by_name(home_team_input, away_team_input):
    # 0. OBȚINERE NUME OFICIAL (PENTRU AFISARE FRUMOASĂ)
    # Chiar daca userul scrie ":real", aici va deveni "Real Madrid"
    home_name_display = get_official_name(home_team_input)
    away_name_display = get_official_name(away_team_input)

    # 1. Scraping (Folosim inputul original sau curățat pentru căutare rank)
    home_rank = get_online_elo(home_team_input)
    away_rank = get_online_elo(away_team_input)

    if home_rank is None: return f"⚠️ Nu am găsit '{home_name_display}'."
    if away_rank is None: return f"⚠️ Nu am găsit '{away_name_display}'."

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

    # --- CALCUL 1: PROBABILITATEA DE VICTORIE ---
    total_goals = goals_h + goals_a + 0.01
    win_prob_h = int((goals_h / total_goals) * 100)
    win_prob_a = int((goals_a / total_goals) * 100)

    # --- CALCUL 2: ÎNCREDEREA AI-ULUI ---
    rank_diff = abs(home_rank - away_rank)
    ai_confidence = 55 + (rank_diff / 4)
    
    goal_diff = abs(goals_h - goals_a)
    if goal_diff > 1.5:
        ai_confidence += 15
        
    ai_confidence = min(98, max(40, int(ai_confidence)))

    # --- GENERARE MESAJ (FOLOSIND NUMELE OFICIALE) ---
    diff = abs(goals_h - goals_a)
    msg_prob = ""

    if diff < 0.35:
        msg_prob = f"Șanse de EGAL: {max(win_prob_h, win_prob_a)}% (Meci Strâns)"
    elif goals_h > goals_a:
        # AICI FOLOSIM home_name_display IN LOC DE home_team_input
        msg_prob = f"Șanse victorie {home_name_display}: {win_prob_h}%"
    else:
        # AICI FOLOSIM away_name_display IN LOC DE away_team_input
        msg_prob = f"Șanse victorie {away_name_display}: {win_prob_a}%"

    return {
        "score": f"{score_h} - {score_a}",
        "details": f"Rank UEFA: {home_rank} vs {away_rank}",
        "probability": msg_prob,       
        "prob_value": ai_confidence,   
        "raw_goals": f"(Estimat AI: {goals_h:.2f} vs {goals_a:.2f} goluri)",
        # Putem trimite si numele oficiale in dictionar daca e nevoie in frontend
        "home_team": home_name_display,
        "away_team": away_name_display
    }