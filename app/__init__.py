from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os
from flask_migrate import Migrate

# Chargement des variables d'environnement
load_dotenv()

# Initialisation des extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Configuration
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialisation des extensions avec l'application
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    # Configuration du login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'info'
    
    # Enregistrement des blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.legislative import legislative_bp
    from app.routes.admin import admin_bp
    from app.routes.secretariat import secretariat_bp
    
    app.register_blueprint(auth_bp)
    csrf.exempt(auth_bp)
    app.register_blueprint(main_bp)
    csrf.exempt(main_bp)
    app.register_blueprint(legislative_bp)
    csrf.exempt(legislative_bp)
    app.register_blueprint(admin_bp)
    csrf.exempt(admin_bp)
    app.register_blueprint(secretariat_bp)
    csrf.exempt(secretariat_bp)
    
    # Enregistrement des gestionnaires d'erreurs
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    # Configuration du logger
    from app.utils.logger import setup_logger
    setup_logger(app)
    
    # Création des tables de la base de données
    with app.app_context():
        db.create_all()
        
        # Création d'un utilisateur administrateur par défaut si nécessaire
        from app.models.user import User
        if not User.query.filter_by(role='admin').first():
            admin = User(
                email='admin@parliament.eu',
                role='admin'
            )
            admin.set_password('Admin123!')
            db.session.add(admin)
            db.session.commit()
            app.logger.info('Admin user created')
    
    @app.context_processor
    def inject_csrf_token():
        from flask_wtf.csrf import generate_csrf
        return dict(csrf_token=generate_csrf)
    
    return app 