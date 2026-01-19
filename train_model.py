import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

print(" Se încarcă datele...")
df = pd.read_csv("data/matches.csv")

# Antrenăm strict pe Rank-uri (Valoarea Echipei)
# Fiind date din sezonul curent, Rank-ul reflectă implicit forma actuală!
X = df[['home_rank', 'away_rank']]

print(" Antrenăm Modelele (Sezon 2025-2026)...")

y_home = df['home_goals']
model_home = RandomForestRegressor(n_estimators=100, random_state=42)
model_home.fit(X, y_home)

y_away = df['away_goals']
model_away = RandomForestRegressor(n_estimators=100, random_state=42)
model_away.fit(X, y_away)

joblib.dump(model_home, "model_home_goals.pkl")
joblib.dump(model_away, "model_away_goals.pkl")

print(" Modele actualizate! AI-ul știe acum doar fotbalul din prezent.")