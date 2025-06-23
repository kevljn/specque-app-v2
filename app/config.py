import os
from datetime import timedelta

class Config:
    # Configuration de base
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///parliament.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration de sécurité
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    WTF_CSRF_ENABLED = False  # Désactive CSRF pour les routes API
    
    # Configuration des emails
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # Configuration de l'application
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    
    # Configuration des rôles
    ROLES = {
        'deputy': 'Député',
        'reporter': 'Rapporteur',
        'admin': 'Administrateur'
    }
    
    # Configuration des statuts
    TEXT_STATUSES = {
        'draft': 'Brouillon',
        'in_commission': 'En commission',
        'in_plenary': 'En séance plénière',
        'adopted': 'Adopté',
        'rejected': 'Rejeté'
    }
    
    AMENDMENT_STATUSES = {
        'proposed': 'Proposé',
        'adopted': 'Adopté',
        'rejected': 'Rejeté'
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 