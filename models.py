from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime # <--- Import nou

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # Legătură cu istoricul
    predictions = db.relationship('Prediction', backref='author', lazy=True)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)
    prediction_score = db.Column(db.String(20), nullable=False) # Ex: "2 - 1"
    prediction_result = db.Column(db.String(50), nullable=False) # Ex: "1 (Gazdele)"
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)