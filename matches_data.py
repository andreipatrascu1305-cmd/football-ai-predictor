import requests
from bs4 import BeautifulSoup
import random

def get_todays_matches():
    """
    Încearcă să ia meciuri de pe ESPN.
    Dacă nu merge, generează meciuri 'Fake' dar realiste, ca să nu fie pagina goală.
    """
    # URL ESPN - Programul meciurilor
    url = "https://www.espn.com/soccer/schedule"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    matches = []
    
    try:
        print(f" Caut meciuri pe ESPN ({url})...")
        response = requests.get(url, headers=headers, timeout=6)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # ESPN pune echipele în tabele cu clasa "Table"
            # Căutăm link-urile care conțin numele echipelor
            # De obicei sunt în tag-uri <span> sau <a> în interiorul tabelului
            
            # Strategie: Căutăm toate rândurile de tabel
            rows = soup.find_all('tr', class_='Table__TR')
            
            for row in rows:
                # În fiecare rând, căutăm numele echipelor (link-uri anchor)
                team_links = row.find_all('a', class_='AnchorLink')
                
                # Filtrăm link-urile care par a fi echipe (au /team/ în url)
                teams = [t.get_text() for t in team_links if '/team/' in t.get('href', '')]
                
                # Trebuie să avem exact 2 echipe pe rând (Gazdă vs Oaspete)
                # Uneori ESPN pune și alte linkuri, deci luăm primele 2 unice
                unique_teams = []
                for t in teams:
                    if t not in unique_teams and len(t) > 2: # Evităm prescurtări dubioase
                        unique_teams.append(t)
                
                if len(unique_teams) >= 2:
                    home = unique_teams[0]
                    away = unique_teams[1]
                    
                    matches.append(generate_match_object(home, away))
                    
                    if len(matches) >= 8: # Maxim 8 meciuri
                        break
            
            if matches:
                print(f" Găsit {len(matches)} meciuri pe ESPN.")

    except Exception as e:
        print(f" Eroare ESPN: {e}")

    # --- BACKUP DINAMIC (Dacă netul eșuează) ---
    if not matches:
        print(" Nu am găsit meciuri online. Generez meciuri simulate.")
        matches = generate_fake_matches()

    return matches

def generate_match_object(home, away):
    """
    Funcție ajutătoare care primește numele și pune cote.
    """
    # Cote random pentru aspect
    seed = random.random()
    if seed < 0.4: # Favorit Gazda
        odd_1 = round(random.uniform(1.4, 1.9), 2)
        odd_x = round(random.uniform(3.2, 3.8), 2)
        odd_2 = round(random.uniform(3.5, 6.0), 2)
    elif seed < 0.7: # Echilibrat
        odd_1 = round(random.uniform(2.2, 2.8), 2)
        odd_x = round(random.uniform(2.9, 3.3), 2)
        odd_2 = round(random.uniform(2.4, 3.0), 2)
    else: # Favorit Oaspeți
        odd_1 = round(random.uniform(3.0, 5.0), 2)
        odd_x = round(random.uniform(3.2, 3.8), 2)
        odd_2 = round(random.uniform(1.5, 2.1), 2)

    return {
        "home": home,
        "away": away,
        "odd_1": odd_1,
        "odd_x": odd_x,
        "odd_2": odd_2
    }

def generate_fake_matches():
    """
    Creează meciuri RANDOM între echipe mari.
    Se schimbă la fiecare refresh, deci pare LIVE.
    """
    top_teams = [
        "Real Madrid", "Barcelona", "Man City", "Liverpool", "Arsenal", 
        "Bayern Munchen", "Dortmund", "PSG", "Inter Milan", "AC Milan", 
        "Juventus", "Napoli", "Atletico Madrid", "Chelsea", "Tottenham",
        "FCSB", "CFR Cluj", "Univ. Craiova", "Rapid", "Dinamo"
    ]
    
    # Amestecăm lista
    random.shuffle(top_teams)
    
    fake_list = []
    # Facem 5 perechi
    for i in range(0, 10, 2):
        home = top_teams[i]
        away = top_teams[i+1]
        fake_list.append(generate_match_object(home, away))
        
    return fake_list