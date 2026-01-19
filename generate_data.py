import pandas as pd
import numpy as np
import random

def generate_matches(num_matches=5000):
    print(f"🧬 Generăm {num_matches} de meciuri sintetice pentru antrenament...")
    
    data = []
    
    for _ in range(num_matches):
        # 1. Generăm Rank-uri aleatorii (între 1 și 200)
        home_rank = random.randint(1, 200)
        away_rank = random.randint(1, 200)
        
        # 2. Calculăm diferența de valoare
        # Dacă home_rank e mic (bun) și away_rank e mare (slab) => diff e mare pozitiv
        diff = away_rank - home_rank
        
        # 3. Calculăm "Puterea Ofensivă" (Lambda pentru Poisson)
        # Media de goluri în fotbal e cam 1.5 per meci
        # Adăugăm avantajul terenului propriu (+0.3 goluri)
        
        # Puterea Gazdelor: Baza 1.3 + Avantaj Rank + Avantaj Teren
        home_lambda = 1.3 + (diff * 0.015) + 0.3
        
        # Puterea Oaspeților: Baza 1.1 - Dezavantaj Rank
        away_lambda = 1.1 - (diff * 0.015)
        
        # Ne asigurăm că nu e negativ (o echipă nu poate da -1 goluri)
        home_lambda = max(0.1, home_lambda)
        away_lambda = max(0.1, away_lambda)
        
        # 4. Generăm scorul folosind Distribuția Poisson (Simulare realistă)
        # Asta face ca 2-1 să fie mai probabil decât 10-5
        home_goals = np.random.poisson(home_lambda)
        away_goals = np.random.poisson(away_lambda)
        
        # 5. Determinăm rezultatul (1, X, 2)
        if home_goals > away_goals:
            result = 1
        elif away_goals > home_goals:
            result = 2
        else:
            result = 0 # X
            
        data.append([home_rank, away_rank, home_goals, away_goals, result])
        
    # Creăm DataFrame-ul
    df = pd.DataFrame(data, columns=['home_rank', 'away_rank', 'home_goals', 'away_goals', 'result'])
    
    # Salvăm în CSV
    df.to_csv("data/matches.csv", index=False)
    print("✅ Gata! Fișierul 'data/matches.csv' are acum date noi și multe.")

if __name__ == "__main__":
    generate_matches()