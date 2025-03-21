from flask import Flask  # Flask-App-Framework
from flask_sqlalchemy import SQLAlchemy  # ORM für Datenbankzugriff
from os import path  # für Dateipfad-Überprüfung (hier ungenutzt)
from flask_login import LoginManager  # für Login-Management

db = SQLAlchemy()  # Datenbank-Instanz
DB_NAME = "todo.db"  # Name für SQLite (hier nicht aktiv)

def create_app():
    app = Flask(__name__)  # App-Instanz erstellen
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'  # Schlüssel für Session-Sicherheit
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://JanHansen:Welcome2024$@JanHansen.mysql.pythonanywhere-services.com:3306/JanHansen$todo'  # MySQL-Verbindungsstring
    db.init_app(app)  # DB mit App verknüpfen

    from views import views  # Views importieren
    from auth import auth  # Authentifizierungsrouten importieren

    app.register_blueprint(views, url_prefix='/')  # Views registrieren
    app.register_blueprint(auth, url_prefix='/')  # Auth registrieren

    from models import User, Note  # Modelle importieren

    with app.app_context():
        db.create_all()  # Tabellen erstellen, falls nicht vorhanden

    login_manager = LoginManager()  # LoginManager-Instanz
    login_manager.login_view = 'auth.login'  # Weiterleitung bei nicht eingeloggtem Zugriff
    login_manager.init_app(app)  # LoginManager mit App verknüpfen

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Nutzer anhand ID laden

    return app  # App zurückgeben
