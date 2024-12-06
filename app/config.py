from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', False)
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
