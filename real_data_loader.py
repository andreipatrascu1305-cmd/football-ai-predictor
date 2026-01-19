import pandas as pd
import requests
import io
import os

# Încercăm să importăm baza de date pentru conversia numelor
try:
    from online_data import BACKUP_DB
except ImportError:
    BACKUP_DB = {} 
    print("⚠️ Atenție: Nu am putut importa BACKUP_DB.")

def download_real_data():
    print("🌍 [2026] Descarc date REALE DOAR din Sezonul Curent (2025-2026)...")
    
    # URL-uri doar pentru sezonul 2526
    urls = [
        "https://www.football-data.co.uk/mmz4281/2526/E0.csv", # Anglia
        "https://www.football-data.co.uk/mmz4281/2526/SP1.csv", # Spania
        "https://www.football-data.co.uk/mmz4281/2526/I1.csv",  # Italia
        "https://www.football-data.co.uk/mmz4281/2526/D1.csv",  # Germania
        "https://www.football-data.co.uk/mmz4281/2526/F1.csv",  # Franța
        "https://www.football-data.co.uk/mmz4281/2526/N1.csv",  # Olanda
        "https://www.football-data.co.uk/mmz4281/2526/P1.csv",  # Portugalia
    ]
    
    all_matches = []
    
    for url in urls:
        try:
            print(f"⬇️ Descarc: {url} ...")
            s = requests.get(url, timeout=10).content
            df = pd.read_csv(io.StringIO(s.decode('utf-8')))
            
            if 'HomeTeam' in df.columns and 'FTHG' in df.columns:
                df = df[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
                all_matches.append(df)
            else:
                print(f"⚠️ Format necunoscut, sar peste.")
                
        except Exception as e:
            print(f"⚠️ Eroare la {url}: {e}")

    if not all_matches:
        print("❌ Nu am putut descărca date. Verifică netul.")
        return

    full_df = pd.concat(all_matches)
    
    # --- Conversie Nume -> Rank ---
    def get_rank(name):
        if not isinstance(name, str): return 150
        clean = name.lower().replace(" ", "").replace("fc", "").replace("cf", "")
        
        if clean in BACKUP_DB: return BACKUP_DB[clean]
        for key, val in BACKUP_DB.items():
            if clean in key or key in clean: return val
        return 150

    full_df['home_rank'] = full_df['HomeTeam'].apply(get_rank)
    full_df['away_rank'] = full_df['AwayTeam'].apply(get_rank)
    full_df['home_goals'] = pd.to_numeric(full_df['FTHG'], errors='coerce')
    full_df['away_goals'] = pd.to_numeric(full_df['FTAG'], errors='coerce')
    
    # Păstrăm doar datele curate, FĂRĂ FORMĂ
    final_df = full_df[['home_rank', 'away_rank', 'home_goals', 'away_goals']]
    final_df = final_df.dropna()
    
    final_df.to_csv("data/matches.csv", index=False)
    print(f"✅ Gata! Avem {len(final_df)} meciuri RECENTE (2025-2026).")
    print("🚀 Rulează acum 'python train_model.py'!")

if __name__ == "__main__":
    download_real_data()