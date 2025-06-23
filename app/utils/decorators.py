from functools import wraps
from flask import abort, current_app, flash, redirect, url_for
from flask_login import current_user

def role_required(role):
    """Décorateur pour vérifier le rôle de l'utilisateur"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Veuillez vous connecter.', 'error')
                return redirect(url_for('auth.login'))
            if current_user.role != role and current_user.role != 'admin':
                flash('Accès refusé : vous n\'avez pas le droit d\'accéder à cette page.', 'error')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Décorateur pour vérifier si l'utilisateur est administrateur"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Accès refusé : seuls les administrateurs peuvent accéder à cette page.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def reporter_required(f):
    """Décorateur pour vérifier si l'utilisateur est rapporteur"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_reporter():
            flash('Accès refusé : seuls les rapporteurs peuvent accéder à cette page.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def text_status_required(status):
    """Décorateur pour vérifier le statut d'un texte législatif"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            text_id = kwargs.get('text_id')
            if not text_id:
                abort(400)
            
            text = current_app.models.LegislativeText.query.get_or_404(text_id)
            if text.status != status:
                flash('Accès refusé : statut du texte incorrect.', 'error')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def amendment_status_required(status):
    """Décorateur pour vérifier le statut d'un amendement"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            amendment_id = kwargs.get('amendment_id')
            if not amendment_id:
                abort(400)
            
            amendment = current_app.models.Amendment.query.get_or_404(amendment_id)
            if amendment.status != status:
                flash('Accès refusé : statut de l\'amendement incorrect.', 'error')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator 