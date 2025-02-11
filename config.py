# config.py
from datetime import timedelta

class Config:
    # Database configuration
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_NAME = 'house_rental'
    
    # JWT configuration
    JWT_SECRET_KEY = 'your-super-secret-key-change-this'  # Change this in production!
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    
    # Flask configuration
    DEBUG = True
    SECRET_KEY = 'another-secret-key-change-this'  # Change this in production!