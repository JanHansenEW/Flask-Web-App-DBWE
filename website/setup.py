from flask import Flask  # Flask-App importieren
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy für DB-Verbindung
from os import path  # Für Dateipfade (hier optional)
from flask_login import LoginManager  # Login-Management

db = SQLAlchemy()  # Datenbankinstanz
DB_NAME = "todo.db"  # Name der Datenbankdatei (nur bei SQLite)

def create_app():
    app = Flask(__name__)  # Flask-App erzeugen
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'  # Schlüssel für Sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://JanHansen:Welcome2024$@JanHansen.mysql.pythonanywhere-services.com:3306/JanHansen$todo'  # MySQL-Verbindungsdaten
    db.init_app(app)  # DB mit App verknüpfen

    from views import views  # Views importieren (Startseite, Notizen)
    from auth import auth  # Authentifizierung importieren

    app.register_blueprint(views, url_prefix='/')  # Views registrieren
    app.register_blueprint(auth, url_prefix='/')  # Auth-Routen registrieren

    from models import User, Note  # Datenmodelle importieren

    with app.app_context():
        db.create_all()  # Tabellen in DB erstellen (falls nicht vorhanden)

    login_manager = LoginManager()  # LoginManager initialisieren
    login_manager.login_view = 'auth.login'  # Weiterleitung bei nicht-eingeloggt
    login_manager.init_app(app)  # LoginManager mit App verknüpfen

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Nutzer anhand ID laden

    return app  # App zurückgeben

#def create_database(app):  # (für SQLite, hier ungenutzt)
#    if not path.exists('website/' + DB_NAME):  # Prüfen ob Datei existiert
#        db.create_all(app=app)  # Datenbank anlegen
#        print('Created Database!')  # Hinweis ausgeben
