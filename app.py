from flask import Flask
from config import Config
from notes.routes import notes_bp
from models import db

def create_app()-> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(notes_bp)    
    return app

