import requests
from bs4 import BeautifulSoup

# --- BACKUP DE URGENȚĂ (Dacă totul pică la prezentare) ---
BACKUP_DB = {
    "mancity": 1, "realmadrid": 2, "liverpool": 3, "inter": 4, 
    "arsenal": 5, "barcelona": 6, "psg": 7, "bayern": 8,
    "fcsb": 100, "cfrcluj": 110, "craiova": 120, "rapid": 130
}

def get_online_elo(team_name):
    """
    Scraping 'Brute Force' pe clasamentul UEFA.
    Citește orice rând din tabel, indiferent de cum e scris codul HTML.
    """
    # Link către clasamentul 2025 (stabil)
    url = "https://kassiesa.net/uefa/data/method5/trank2026.html"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        print(f"📡 Scraping pe: {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- SCHIMBARE MAJORĂ: Luăm absolut TOATE rândurile din pagină ---
        # Nu mai căutăm clase specifice care se pot schimba.
        rows = soup.find_all('tr')
        
        print(f"✅ Conectat! Analizez {len(rows)} rânduri de date...")

        # Pregătim numele căutat
        clean_input = team_name.lower().replace(" ", "").strip()
        
        # Mapare Nume (Tu -> Site)
        mapping = {
            "mancity": "mancity",      
            "manchestercity": "mancity",
            "manchesterunited": "manutd",
            "realmadrid": "realmadrid",
            "barcelona": "barcelona",
            "barca": "barcelona",
            "fcsb": "fcsb",
            "steaua": "fcsb",
            "cfr": "cfrcluj",
            "cfrcluj": "cfrcluj",
            "rapid": "rapidbucuresti",
            "dinamo": "dinamobucuresti"
        }
        target = mapping.get(clean_input, clean_input)
        
        # Căutăm în fiecare rând
        for row in rows:
            # Luăm tot textul din rând, eliminăm spațiile și punctele
            # Ex: "1 Man City Eng 120.000" devine "1mancityeng120000"
            text = row.get_text().lower().replace(" ", "").replace(".", "").replace("\n", "")
            
            # Verificăm dacă numele țintă e acolo
            if target in text:
                # Încercăm să extragem numărul de la început (Rank-ul)
                try:
                    # Găsim coloanele rândului
                    cols = row.find_all('td')
                    if cols and len(cols) > 0:
                        rank_text = cols[0].get_text().strip()
                        if rank_text.isdigit():
                            rank = int(rank_text)
                            print(f"🎉 GĂSIT PE NET! {team_name} -> Locul {rank}")
                            return rank
                except:
                    continue # Dacă dă eroare la un rând, trecem la următorul

        print("⚠️ Nu am găsit pe site, trec pe Backup...")
        
    except Exception as e:
        print(f"⚠️ Eroare conexiune ({e}). Trec pe Backup...")

    # --- PLAN B: BACKUP ---
    # Dacă scraping-ul eșuează sau nu găsește echipa, folosim lista locală
    if clean_input in BACKUP_DB:
        print(f"📂 Folosesc date interne: {clean_input} -> {BACKUP_DB[clean_input]}")
        return BACKUP_DB[clean_input]
    
    # Dacă nici în backup nu e, returnăm un rank mediu (50) ca să nu crape
    return 50