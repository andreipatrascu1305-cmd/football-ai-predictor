import pandas as pd
from sklearn.ensemble import RandomForestRegressor # Folosim Regresie, nu Clasificare
import joblib

print("⏳ Se încarcă datele...")
df = pd.read_csv("data/matches.csv")

X = df[['home_rank', 'away_rank']]

# --- MODEL 1: Prezice câte goluri dă GAZDA ---
print("🤖 Antrenăm Modelul 1 (Goluri Gazdă)...")
y_home = df['home_goals']
model_home = RandomForestRegressor(n_estimators=100, random_state=42)
model_home.fit(X, y_home)

# --- MODEL 2: Prezice câte goluri dau OASPEȚII ---
print("🤖 Antrenăm Modelul 2 (Goluri Oaspeți)...")
y_away = df['away_goals']
model_away = RandomForestRegressor(n_estimators=100, random_state=42)
model_away.fit(X, y_away)

# Salvăm ambele modele
joblib.dump(model_home, "model_home_goals.pkl")
joblib.dump(model_away, "model_away_goals.pkl")

print("✅ Modelele au fost salvate cu succes!")
print("Acum AI-ul știe să prezică scoruri exacte (ex: 3-1).")