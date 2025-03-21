from setup import db  # Datenbankinstanz importieren
from flask_login import UserMixin  # Für Login-Integration mit User-Modell
from sqlalchemy.sql import func  # Für automatische Zeitstempel

class Note(db.Model):  # Datenbankmodell für Notizen
    id = db.Column(db.Integer, primary_key=True)  # Primärschlüssel
    data = db.Column(db.String(10000))  # Inhalt der Notiz (max. 10.000 Zeichen)
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # Zeitstempel, wann erstellt
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Fremdschlüssel zum User

class User(db.Model, UserMixin):  # Datenbankmodell für Nutzer
    id = db.Column(db.Integer, primary_key=True)  # Primärschlüssel
    email = db.Column(db.String(150), unique=True)  # E-Mail-Adresse (eindeutig)
    password = db.Column(db.String(150))  # Gehashtes Passwort
    first_name = db.Column(db.String(150))  # Vorname
    notes = db.relationship('Note')  # Beziehung zu Notizen (1:N)
