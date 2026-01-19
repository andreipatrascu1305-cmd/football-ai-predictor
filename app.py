from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Prediction
from forms import LoginForm, RegisterForm, PredictForm
# Importăm funcția care caută pe net
from ml_model import get_prediction_by_name
# Importăm funcția pentru meciurile de azi
from matches_data import get_todays_matches 
from flask import make_response
from news_data import get_latest_news
import io
import os
import csv
app = Flask(__name__)

app.config['SECRET_KEY'] = 'cheie-secreta-foarte-greu-de-ghicit'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# Acest cod va rula DE FIECARE DATĂ când pornește serverul (și pe Render)
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- RUTE ---
@app.route('/')
def home():
    # DACĂ ești deja logat, te trimit direct la Predicții (Dashboard)
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # DACĂ NU ești logat, îți arăt pagina de prezentare (Home)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Cont creat cu succes!', 'success')
            return redirect(url_for('login'))
        except:
            flash('Userul sau emailul există deja.', 'danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Date incorecte.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = PredictForm()
    prediction_data = None
    
    # 1. Luăm meciurile zilei
    todays_matches = get_todays_matches()
    latest_news = get_latest_news()

    # 2. Auto-Fill din URL
    if request.method == 'GET' and request.args.get('home'):
        form.home_team.data = request.args.get('home')
        form.away_team.data = request.args.get('away')

    if form.validate_on_submit():
        # Curățăm datele (litere mici, fără spații inutile, prima literă mare)
        home_clean = form.home_team.data.strip().title()
        away_clean = form.away_team.data.strip().title()

        # --- LOGIC CHECK (BREAK FAIL) ---
        # Comparăm versiunile lowercase ca să fim siguri
        if home_clean.lower() == away_clean.lower():
            flash('🦄 Alooo! Echipele trebuie să fie diferite! Nu se pot juca cu ele însele (decât la antrenament).', 'warning')
            return render_template('dashboard.html', form=form, matches=todays_matches,news=latest_news)

        # --- AICI ERA GREȘEALA ---
        # Acum folosim variantele curățate (home_clean), nu datele brute din formular
        home_name = home_clean
        away_name = away_clean
        
        prediction_data = get_prediction_by_name(home_name, away_name)
        
        # Salvăm în istoric
        if isinstance(prediction_data, dict):
            new_pred = Prediction(
                home_team=home_name, # Acum va salva "Barcelona" nu "barcelona"
                away_team=away_name,
                prediction_score=prediction_data['score'],
                prediction_result=prediction_data['probability'],
                author=current_user
            )
            db.session.add(new_pred)
            db.session.commit()
        
    return render_template('dashboard.html', form=form, prediction=prediction_data, matches=todays_matches, news=latest_news)

@app.route('/history')
@login_required
def history():
    # 1. Luăm predicțiile
    preds = Prediction.query.filter_by(author=current_user).order_by(Prediction.date_posted.desc()).all()
    
    # 2. CALCULĂM STATISTICILE (BAZAT PE SCOR)
    count_1 = 0
    count_x = 0
    count_2 = 0
    
    for p in preds:
        try:
            # Scorul este salvat ca string: "2 - 1" sau "0 - 0"
            # Îl spargem la liniuță
            parts = p.prediction_score.split('-') 
            
            if len(parts) == 2:
                home_goals = int(parts[0].strip()) # Primul număr
                away_goals = int(parts[1].strip()) # Al doilea număr
                
                if home_goals > away_goals:
                    count_1 += 1
                elif away_goals > home_goals:
                    count_2 += 1
                else:
                    count_x += 1
        except:
            continue # Dacă e vreo eroare la un rând, trecem peste el

    # 3. Trimitem datele la HTML
    return render_template('history.html', predictions=preds, c1=count_1, cx=count_x, c2=count_2)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Te-ai delogat cu succes.', 'info')
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/download_report')
@login_required
def download_report():
    # 1. Luăm datele din DB
    preds = Prediction.query.filter_by(author=current_user).all()
    
    # 2. Creăm un răspuns tip CSV
    si = io.StringIO()
    cw = csv.writer(si)
    
    # Scriem capul de tabel
    cw.writerow(['Data', 'Echipa Gazda', 'Echipa Oaspete', 'Scor Prezumat', 'Rezultat'])
    
    # Scriem rândurile
    for p in preds:
        cw.writerow([p.date_posted, p.home_team, p.away_team, p.prediction_score, p.prediction_result])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=istoric_predictii.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/admin')
@login_required
def admin():
    # VERIFICARE DE SECURITATE: Doar tu (id=1) ai voie aici!
    if current_user.id != 1:
        flash("Nu ai acces aici! Această zonă este doar pentru Administratori.", "danger")
        return redirect(url_for('dashboard'))
    
    # Luăm toți userii
    all_users = User.query.all()
    return render_template('admin.html', users=all_users)

if __name__ == '__main__':
    with app.app_context():
        # Verificăm dacă baza de date există
        if not os.path.exists('database.db'):
            db.create_all()
            print("Baza de date a fost creată!")
            
    # Pornim serverul
    print(" Serverul pornește pe http://127.0.0.1:5000")
    app.run(debug=True)