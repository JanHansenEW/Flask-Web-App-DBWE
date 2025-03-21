from flask import Blueprint, render_template, request, flash, jsonify  # Flask-Funktionen
from flask_login import login_required, current_user  # Login-Zugriff und aktueller Nutzer
from models import Note, User  # Datenmodelle
from setup import db  # Datenbankinstanz
import json  # Für JSON-Verarbeitung
import smtplib  # Zum Versenden von E-Mails
from email.mime.multipart import MIMEMultipart  # Für E-Mail-Nachricht (HTML)
from email.mime.text import MIMEText  # Für HTML-Inhalt in E-Mail
from_address = "j.hansen.pythonanywhere@gmail.com"  # Absenderadresse

views = Blueprint('views', __name__)  # Blueprint für Views (Startseite, Notizen)

def send_email(to_user, body, subject):  # E-Mail-Funktion
    to_address = to_user.email  # Empfängeradresse
    msg = MIMEMultipart('alternative')  # Multipart-Nachricht erzeugen
    msg['Subject'] = subject  # Betreff setzen
    msg['From'] = from_address  # Absenderadresse
    msg['To'] = to_address  # Empfängeradresse

    html = body  # HTML-Inhalt der Nachricht
    part1 = MIMEText(html, 'html')  # HTML als MIME-Typ

    msg.attach(part1)  # Inhalt zur Nachricht hinzufügen

    username = from_address  # E-Mail-Login
    password = 'sekq aqrs nybl bzja'  # App-Passwort

    # Senden der mail
    # Diese smtp config funnktioniert für mich, wurde mit googlen ermittelt
    server = smtplib.SMTP('smtp.gmail.com', 587)  # SMTP-Verbindung starten
    server.ehlo()  # Server begrüßen
    server.starttls()  # TLS aktivieren
    server.login(username, password)  # Einloggen
    server.sendmail(from_address, to_address, msg.as_string())  # E-Mail senden
    server.quit()  # Verbindung schließen

@views.route('/', methods=['GET'])  # Route für Startseite (GET)
@login_required  # Nur für eingeloggte Nutzer
def get_home():
    return render_template("home.html", user=current_user)  # Startseite anzeigen

@views.route('/', methods=['POST'])  # Route zum Erstellen von Notizen (POST)
@login_required  # Nur für eingeloggte Nutzer
def create_note():
    note = request.form.get('note')  # Notiztext aus Formular holen

    if len(note) < 1:
        flash('Note is too short!', category='error')  # Fehlermeldung bei leerer Eingabe
    else:
        new_note = Note(data=note, user_id=current_user.id)  # Neue Notiz erstellen
        db.session.add(new_note)  # Zur DB hinzufügen
        db.session.commit()  # Speichern
        flash('Note added!', category='success')  # Erfolgsmeldung
        email_message = f'Neues Todo "{note}"'  # E-Mail-Inhalt
        send_email(current_user, email_message, 'Neues ToDo')  # E-Mail senden

    return render_template("home.html", user=current_user)  # Seite neu laden

@views.route('/delete-note', methods=['POST'])  # Route zum Löschen von Notizen
def delete_note():
    note = json.loads(request.data)  # JSON-Daten vom Client (JavaScript)
    noteId = note['noteId']  # ID extrahieren
    note = Note.query.get(noteId)  # Notiz aus DB laden
    if note:
        if note.user_id == current_user.id:  # Nur eigene Notizen dürfen gelöscht werden
            db.session.delete(note)  # Notiz löschen
            db.session.commit()  # Änderungen speichern
            email_message = f'ToDo  "{note.data}" wurde entfernt'  # E-Mail-Inhalt
            send_email(current_user, email_message, "ToDo entfernt")  # E-Mail senden

    return jsonify({})  # Leere JSON-Antwort zurückgeben
