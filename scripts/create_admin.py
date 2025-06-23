import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from app import create_app, db
from app.models.user import User

def create_admin_user(email, password):
    app = create_app()
    with app.app_context():
        # Vérifier si un administrateur existe déjà
        if User.query.filter_by(role='admin').first():
            print("Un administrateur existe déjà dans la base de données.")
            return

        # Vérifier si l'email est déjà utilisé
        if User.query.filter_by(email=email).first():
            print(f"L'email {email} est déjà utilisé.")
            return

        # Créer le compte administrateur
        admin = User(email=email, role='admin')
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"Compte administrateur créé avec succès pour {email}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python create_admin.py <email> <password>")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    create_admin_user(email, password) 