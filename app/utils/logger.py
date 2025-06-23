import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
        
    # Configuration du logger
    file_handler = RotatingFileHandler(
        'logs/parliament.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Ajout du handler au logger de l'application
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Parliament startup')

def log_user_action(user, action, details=None):
    """Log une action utilisateur"""
    message = f"User {user.email} ({user.role}) performed action: {action}"
    if details:
        message += f" - Details: {details}"
    current_app.logger.info(message)

def log_system_event(event, details=None):
    """Log un événement système"""
    message = f"System event: {event}"
    if details:
        message += f" - Details: {details}"
    current_app.logger.info(message)

def log_error(error, context=None):
    """Log une erreur"""
    message = f"Error: {str(error)}"
    if context:
        message += f" - Context: {context}"
    current_app.logger.error(message) 