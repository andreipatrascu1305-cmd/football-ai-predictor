import feedparser

def get_latest_news():
    """
    Preluăm ultimele știri de pe DigiSport (RSS Feed).
    Este rapid, legal și nu blochează serverul.
    """
    # RSS Feed oficial DigiSport Fotbal
    rss_url = "https://www.digisport.ro/rss/fotbal"
    
    news_list = []
    
    try:
        # Descărcăm fluxul de știri
        feed = feedparser.parse(rss_url)
        
        # Luăm primele 5 știri
        for entry in feed.entries[:5]:
            # Uneori imaginile sunt ascunse în structuri complexe, 
            # așa că luăm doar Titlul, Linkul și Descrierea scurtă pentru simplitate.
            news_list.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary.split('<')[0] # Curățăm tag-urile HTML dacă există
            })
            
    except Exception as e:
        print(f"Eroare RSS: {e}")
        # Backup în caz de eroare
        news_list = [
            {"title": "Vezi ultimele noutăți pe DigiSport.ro", "link": "https://www.digisport.ro", "summary": "Click pentru a accesa site-ul."},
        ]

    return news_list