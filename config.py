from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///exam.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
