from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from models import db
from scheduler import start_scheduler

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///parking.db"
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    start_scheduler(app)

    return app, login_manager
