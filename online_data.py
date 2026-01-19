import requests
from bs4 import BeautifulSoup

# ==========================================
#  BACKUP DB (600+ Echipe)
# Include Ligi Secunde, America de Sud, Arabia, etc.
# ==========================================
BACKUP_DB = {
    # --- TOP GIANTS (1-50) ---
    "mancity": 1, "manchestercity": 1,
    "realmadrid": 2, "real": 2,
    "bayern": 3, "bayernmunchen": 3,
    "liverpool": 4,
    "arsenal": 5,
    "inter": 6, "intermilano": 6,
    "psg": 7,
    "leverkusen": 8,
    "barcelona": 9, "barca": 9,
    "dortmund": 10,
    "atleticomadrid": 11, "atletico": 11,
    "rb leipzig": 12, "leipzig": 12,
    "chelsea": 13,
    "napoli": 14,
    "juventus": 15, "juve": 15,
    "acmilan": 16, "milan": 16,
    "tottenham": 17, "spurs": 17,
    "astonvilla": 18,
    "newcastle": 19,
    "manutd": 20, "manchesterunited": 20,
    "benfica": 21,
    "porto": 22,
    "sporting": 23, "sportinglisabona": 23,
    "atalanta": 24,
    "roma": 25, "asroma": 25,
    "lazio": 26,
    "feyenoord": 27,
    "psv": 28,
    "sevilla": 29,
    "realsociedad": 30,
    "villareal": 31, "villarreal": 31,
    "lille": 32,
    "monaco": 33,
    "marseille": 34,
    "lens": 35,
    "brighton": 36,
    "westham": 37,
    "bologna": 38,
    "girona": 39,
    "athleticbilbao": 40, "bilbao": 40,
    "stuttgart": 41,
    "frankfurt": 42,
    "fiorentina": 43,
    "galatasaray": 44,
    "fenerbahce": 45,
    "shakhtar": 46,
    "olympiacos": 47,
    "rangers": 48,
    "celtic": 49,
    "salzburg": 50, "rbsalzburg": 50,

    # --- MID TIER & ANGLIA (Premier + Championship) ---
    "fulham": 60, "bournemouth": 62, "crystalpalace": 65,
    "wolves": 68, "wolverhampton": 68, "everton": 70,
    "brentford": 72, "nottingham": 75, "forest": 75,
    "leicester": 80, "leicestercity": 80,
    "leeds": 85, "leedsunited": 85,
    "southampton": 88,
    "ipswich": 90, "ipswichTown": 90,
    "norwich": 100, "westbrom": 102, "coventry": 105,
    "middlesbrough": 110, "hull": 112, "hullcity": 112,
    "sunderland": 115, "watford": 118, "preston": 120,
    "bristolcity": 125, "cardiff": 130, "swansea": 132,
    "stoke": 135, "stokecity": 135, "qpr": 140,
    "blackburn": 145, "sheffieldwed": 150, "plymouth": 155,

    # --- SPANIA (La Liga + Segunda) ---
    "betis": 55, "realbetis": 55,
    "valencia": 70,
    "osasuna": 75, "mallorca": 80,
    "rayovallecano": 85, "rayo": 85,
    "getafe": 90, "celta": 92, "celtavigo": 92,
    "alaves": 95, "laspalmas": 98,
    "cadiz": 105, "granada": 108, "almeria": 110,
    "valladolid": 115, "realvalladolid": 115,
    "espanyol": 118,
    "eibar": 120, "leganes": 122,
    "elche": 125, # <--- AICI ESTE ELCHE
    "levante": 128, "sportinggijon": 130,
    "oviedo": 132, "racing": 135, "burgos": 138,
    "tenerife": 140, "zaragoza": 145, "huesca": 150,

    # --- ITALIA (Serie A + Serie B) ---
    "torino": 70, "monza": 75, "genoa": 78,
    "udinese": 82, "sassuolo": 85, "lecce": 90,
    "cagliari": 92, "verona": 95, "empoli": 98,
    "salernitana": 100, "frosinone": 102,
    "parma": 105, "como": 108, "venezia": 110,
    "cremonese": 112, "palermo": 115, "sampdoria": 120,
    "brescia": 125, "bari": 130, "pisa": 135,

    # --- GERMANIA (Bundesliga + 2.BuLi) ---
    "freiburg": 55, "hoffenheim": 65, "augsburg": 75,
    "werder": 80, "werderbremen": 80, "wolfsburg": 82,
    "gladbach": 85, "borussiamg": 85,
    "heidenheim": 90, "bochum": 95, "unionberlin": 98,
    "mainz": 100, "cologne": 105, "koln": 105,
    "darmstadt": 108,
    "stpauli": 110, "holsteinkiel": 112,
    "hamburg": 115, "hsv": 115,
    "fortuna": 118, "dusseldorf": 118,
    "hannover": 120, "karlsruhe": 122,
    "hertha": 125, "herthaberlin": 125,
    "schalke": 130, "schalke04": 130,
    "nurnberg": 140,

    # --- FRANTA (Ligue 1 + Ligue 2) ---
    "nice": 60, "rennes": 62, "lyon": 65,
    "reims": 75, "toulouse": 80, "strasbourg": 85,
    "montpellier": 90, "nantes": 95, "lorient": 98,
    "metz": 100, "lehavre": 102,
    "auxerre": 110, "angers": 112, "stetienne": 115, "saintetienne": 115,
    "bordeaux": 120, "paris": 125, "parisfc": 125,

    # --- ROMANIA (Superliga) ---
    "fcsb": 100, "steaua": 100,
    "cfrcluj": 110, "cfr": 110,
    "universitateacraiova": 120, "craiova": 120, "univcraiova": 120,
    "rapid": 130, "rapidbucuresti": 130,
    "farul": 140, "farulconstanta": 140, "viitorul": 140,
    "sepsi": 150, "osk": 150,
    "ucluj": 155, "universitateacluj": 155,
    "hermannstadt": 160,
    "uta": 165, "utaarad": 165,
    "petrolul": 170,
    "otelul": 175,
    "poliiasi": 180,
    "voluntari": 190,
    "dinamo": 200, "dinamobucuresti": 200,
    "fcbotosani": 210, "botosani": 210,
    "fcucraiova": 220, "craiova1948": 220,
    "unireaslobozia": 230,
    "gloriabuzau": 240,
    "corvinul": 250,

    # --- ALTELE EUROPA (Turcia, Grecia, Belgia, Olanda, Portugalia etc.) ---
    "besiktas": 65, "trabzonspor": 80, "basaksehir": 90,
    "paok": 70, "aek": 80, "panathinaikos": 85, "aris": 120,
    "brugge": 50, "clubbrugge": 50, "unionstgilloise": 60,
    "anderlecht": 70, "gent": 75, "genk": 80, "antwerp": 85,
    "twente": 60, "az": 65, "utrecht": 100,
    "braga": 50, "vitoria": 100, "famalicao": 120,
    "youngboys": 70, "servette": 110, "lugano": 120,
    "sturm": 80, "lask": 100, "rapidwien": 110,
    "dinamozagreb": 60, "hajduk": 120, "rijeka": 130,
    "copenhaga": 60, "midtjylland": 80, "nordsjaelland": 100,
    "bodo": 70, "molde": 90,
    "malmo": 100, "djurgarden": 140,
    "legia": 110, "lech": 115, "rakow": 120,
    "ferencvaros": 80,
    "ludogorets": 85,
    "sheriff": 100,
    "apoel": 130,

    # --- REST OF THE WORLD (Pt amicale sau meciuri mari) ---
    "intermiami": 150, "miami": 150,
    "alnassr": 90, "alhilal": 80, "alittihad": 95,
    "flamengo": 60, "palmeiras": 65, "saopaulo": 80,
    "riverplate": 70, "bocajuniors": 75,
    "river": 70, "boca": 75
}

def get_online_elo(team_name):  
    url = "https://kassiesa.net/uefa/data/method5/trank2026.html"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    clean_input = team_name.lower().replace(" ", "").replace("-", "").strip()
    
    scraping_map = {
        "mancity": "mancity", "manutd": "manutd",
        "elche": "elche", "sevilla": "sevilla",
        "fcsb": "fcsb", "steaua": "fcsb",
        "cfr": "cfrcluj", "rapid": "rapidbucuresti",
        "craiova": "univcraiova", "realmadrid": "realmadrid"
    }
    target_for_site = scraping_map.get(clean_input, clean_input)

    try:
        # MESAJ PROFESIONAL 1: Conexiune
        print(f" [NET] Conectare la UEFA Live Data ({url})...")
        response = requests.get(url, headers=headers, timeout=4)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rows = soup.find_all('tr')
        
        # MESAJ PROFESIONAL 2: Analiza Datelor
        print(f" [OK] Conexiune stabilita. Analizez {len(rows)} echipe din clasament...")
        
        for row in rows:
            row_text = row.get_text().lower().replace(" ", "").replace(".", "")
            
            if target_for_site in row_text:
                cols = row.find_all('td')
                if cols:
                    rank_text = cols[0].get_text().strip()
                    if rank_text.isdigit():
                        rank = int(rank_text)
                        print(f"🌟 [SUCCESS] Echipa gasita online: {team_name} -> Rank {rank}")
                        return rank
                        
    except Exception as e:
        print(f"⚠️ [WARNING] Eroare conexiune: {e}")

    # --- ZONA BACKUP ---
    # Mesaj care explică DE CE trecem pe backup (nu e eroare, e logică)
    print(f" [INFO] Echipa '{team_name}' nu este în Top 500 UEFA. Comut pe Baza de Date Extinsă...")
    
    if clean_input in BACKUP_DB:
        print(f"📂 [BACKUP] Găsit în sistem local: Rank {BACKUP_DB[clean_input]}")
        return BACKUP_DB[clean_input]
    
    for key, val in BACKUP_DB.items():
        if clean_input in key or key in clean_input:
            print(f" [BACKUP] Găsit prin aproximare ({key}): Rank {val}")
            return val

    print(" [ERROR] Echipa necunoscută. Se atribuie Rank Mediu (150).")
    return 150
# ==========================================
# 🆕 SECTIUNE NOUA: FORMATARE NUME
# ==========================================

# Aici definim cum vrem să arate numele oficial
OFFICIAL_NAMES = {
    # --- ANGLIA ---
    "mancity": "Manchester City", "manchestercity": "Manchester City",
    "manutd": "Manchester United", "manchesterunited": "Manchester United",
    "liverpool": "Liverpool", "arsenal": "Arsenal",
    "chelsea": "Chelsea", "tottenham": "Tottenham", "spurs": "Tottenham",
    "newcastle": "Newcastle", "astonvilla": "Aston Villa",
    "westham": "West Ham", "brighton": "Brighton",
    
    # --- SPANIA ---
    "realmadrid": "Real Madrid", "real": "Real Madrid",
    "barcelona": "FC Barcelona", "barca": "FC Barcelona",
    "atletico": "Atlético Madrid", "atleticomadrid": "Atlético Madrid",
    "sevilla": "Sevilla", "betis": "Real Betis",
    "girona": "Girona", "valencia": "Valencia",
    
    # --- GERMANIA ---
    "bayern": "Bayern München", "bayernmunchen": "Bayern München",
    "dortmund": "Borussia Dortmund", "bvb": "Borussia Dortmund",
    "leverkusen": "Bayer Leverkusen", "leipzig": "RB Leipzig",
    
    # --- ITALIA ---
    "inter": "Inter Milano", "intermilano": "Inter Milano",
    "acmilan": "AC Milan", "milan": "AC Milan",
    "juventus": "Juventus", "juve": "Juventus",
    "napoli": "Napoli", "roma": "AS Roma", "lazio": "Lazio",
    "atalanta": "Atalanta",
    
    # --- FRANT + OTHERS ---
    "psg": "Paris Saint-Germain",
    "benfica": "Benfica", "porto": "FC Porto", "sporting": "Sporting CP",
    
    # --- ROMANIA ---
    "fcsb": "FCSB", "steaua": "FCSB",
    "cfr": "CFR Cluj", "cfrcluj": "CFR Cluj",
    "rapid": "Rapid București", "rapidbucuresti": "Rapid București",
    "craiova": "Univ. Craiova", "universitateacraiova": "Univ. Craiova",
    "farul": "Farul Constanța", "viitorul": "Farul Constanța",
    "dinamo": "Dinamo București", "petrolul": "Petrolul Ploiești",
    "otelul": "Oțelul Galați", "sepsi": "Sepsi OSK",
    "ucluj": "U Cluj",
    
    # --- DIVERSE ---
    "intermiami": "Inter Miami", "alnasr": "Al-Nassr"
}

def get_official_name(user_input):
    """
    Transformă inputul utilizatorului (ex: :real, realmadrid) 
    în numele oficial (ex: Real Madrid).
    """
    # 1. Curățăm inputul exact ca la căutare
    clean = user_input.lower().replace(" ", "").replace("-", "").replace(":", "").strip()
    
    # 2. Căutăm în dicționarul de nume oficiale
    if clean in OFFICIAL_NAMES:
        return OFFICIAL_NAMES[clean]
    
    # 3. Dacă nu e în listă, încercăm să îl facem frumos (Prima literă mare)
    # Ex: "voluntari" -> "Voluntari"
    return user_input.replace(":", "").title()