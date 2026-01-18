from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Utilizator', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Parolă', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmă Parola', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Înregistrează-te')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Parolă', validators=[DataRequired()])
    submit = SubmitField('Logare')

class PredictForm(FlaskForm):
    # AICI AM MODIFICAT: Doar nume, FĂRĂ RANK!
    home_team = StringField('Echipă Gazdă', validators=[DataRequired()])
    away_team = StringField('Echipă Oaspete', validators=[DataRequired()])
    
    submit = SubmitField('Caută pe net și fă Predicția!')