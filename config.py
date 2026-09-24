import os

from dotenv import load_dotenv 
load_dotenv()

class Config: 
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{os.path.join(os.path.dirname(__file__ ), 'db.sqlite3')}"