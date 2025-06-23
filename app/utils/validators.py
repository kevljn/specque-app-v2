import re
from flask import current_app
from werkzeug.security import check_password_hash

def validate_email(email):
    """Valide le format d'un email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """Valide la force d'un mot de passe"""
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    
    if not re.search(r'[A-Z]', password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    
    if not re.search(r'[a-z]', password):
        return False, "Le mot de passe doit contenir au moins une minuscule"
    
    if not re.search(r'\d', password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Le mot de passe doit contenir au moins un caractère spécial"
    
    return True, "Mot de passe valide"

def validate_legislative_text(title, content):
    """Valide un texte législatif"""
    errors = []
    
    if not title or len(title.strip()) < 5:
        errors.append("Le titre doit contenir au moins 5 caractères")
    
    if not content or len(content.strip()) < 50:
        errors.append("Le contenu doit contenir au moins 50 caractères")
    
    return len(errors) == 0, errors

def validate_amendment(content):
    """Valide un amendement"""
    errors = []
    if not content or len(content.strip()) < 10:
        errors.append("Le contenu de l'amendement doit contenir au moins 10 caractères")
    return len(errors) == 0, errors

def validate_vote(vote_type):
    """Valide un vote"""
    valid_types = ['for', 'against', 'abstention']
    if vote_type not in valid_types:
        return False, f"Type de vote invalide. Doit être l'un des suivants : {', '.join(valid_types)}"
    return True, "Vote valide" 