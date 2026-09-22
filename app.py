from flask import Flask
from notes.routes import notes_bp

def create_app()-> Flask:
    app = Flask(__name__)
    app.register_blueprint(notes_bp)    
    return app

