from flask import Blueprint, render_template, request, flash, redirect, url_for  # Flask-Module für Routing & Formulare
from models import User  # Datenmodell User importieren
from werkzeug.security import generate_password_hash, check_password_hash  # Passwort-Hashing
from setup import db  # DB-Instanz importieren
from flask_login import login_user, login_required, logout_user, current_user  # Login-Management

auth = Blueprint('auth', __name__)  # Blueprint für Authentifizierung definieren

@auth.route('/login', methods=['GET'])  # Login-Seite anzeigen
def get_login_page():
    return render_template("login.html", user=current_user)  # Login-Template mit Nutzerkontext

@auth.route('/login', methods=['POST'])  # Login-Formular verarbeiten
def login():
    email = request.form.get('email')  # E-Mail aus Formular holen
    password = request.form.get('password')  # Passwort aus Formular holen

    print(email)  # Debug-Ausgabe
    user = User.query.filter_by(email=email).first()  # Nutzer aus DB laden
    if user:
        if check_password_hash(user.password, password):  # Passwort prüfen
            flash('Logged in successfully!', category='success')  # Erfolgsmeldung
            login_user(user, remember=True)  # Nutzer einloggen
            return redirect(url_for('views.get_home'))  # Weiterleitung zur Startseite
        else:
            flash('Incorrect password, try again.', category='error')  # Falsches Passwort
    else:
        flash('Email does not exist.', category='error')  # E-Mail nicht gefunden

    return render_template("login.html", user=current_user)  # Login-Seite erneut anzeigen

@auth.route('/logout')  # Logout-Route
@login_required  # Nur erreichbar, wenn eingeloggt
def logout():
    logout_user()  # Nutzer ausloggen
    return redirect(url_for('auth.get_login_page'))  # Zurück zur Login-Seite

@auth.route('/sign-up', methods=['GET'])  # Registrierungsseite anzeigen
def get_signup_page():
    return render_template("sign_up.html", user=current_user)  # Template laden

@auth.route('/sign-up', methods=['POST'])  # Registrierung verarbeiten
def sign_up():
    email = request.form.get('email')  # E-Mail holen
    first_name = request.form.get('firstName')  # Vorname holen
    password1 = request.form.get('password1')  # Passwort holen
    password2 = request.form.get('password2')  # Passwort-Wiederholung holen

    user = User.query.filter_by(email=email).first()  # Prüfen, ob E-Mail schon existiert
    if user:
        flash('Email already exists.', category='error')  # Fehlermeldung
    elif len(email) < 4:
        flash('Email must be greater than 3 characters.', category='error')  # Validierung
    elif len(first_name) < 2:
        flash('First name must be greater than 1 character.', category='error')  # Validierung
    elif password1 != password2:
        flash('Passwords don\'t match.', category='error')  # Passwörter ungleich
    elif len(password1) < 7:
        flash('Password must be at least 7 characters.', category='error')  # Passwort zu kurz
    else:
        new_user = User(email=email, first_name=first_name, password=generate_password_hash(
            password1, method='sha256'))  # Neuer User mit gehashtem Passwort
        db.session.add(new_user)  # Zur DB hinzufügen
        db.session.commit()  # Änderungen speichern
        return redirect(url_for('views.get_home'))  # Weiter zur Startseite

    return render_template("sign_up.html", user=current_user)  # Registrierung erneut anzeigen
