from flask import Flask
from flask_alembic import Alembic
from app.config import Config
from app.notes.routes import notes_bp
from app.models.note import db

alembic = Alembic()
def create_app()-> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    alembic.init_app(app)
    db.init_app(app)
    app.register_blueprint(notes_bp)    
    return app

