# Application de Simulation Parlementaire - SPECQUE

Une application web légère et modulaire permettant de simuler le fonctionnement législatif du Parlement européen. Cette application est conçue comme un outil pédagogique pour la SPECQUE afin de comprendre le processus législatif européen.

## Fonctionnalités

- Gestion des utilisateurs avec différents rôles (député, rapporteur, administrateur, secrétariat, chef de groupe, représentant d'intérêt, rapporteur fictif)
- Création et gestion de textes législatifs
- Proposition et vote d'amendements
- Suivi du processus législatif (commission, séance plénière)
- Interface responsive et intuitive
- Système de notifications par email

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Base de données SQLite (incluse) ou PostgreSQL (optionnel)

## Installation

1. Cloner le dépôt :
```bash
git clone [URL_DU_REPO]
cd simulation-parlementaire
```

2. Créer un environnement virtuel :
```bash
python -m venv venv 
python3 -m venv venv #Sur macOS
source venv/bin/activate  # Sur Unix/macOS
# ou
venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer le fichier .env avec vos paramètres :
# - SECRET_KEY : Clé secrète pour les sessions
# - MAIL_SERVER : Serveur SMTP pour les emails
# - MAIL_USERNAME : Nom d'utilisateur SMTP
# - MAIL_PASSWORD : Mot de passe SMTP
# - DATABASE_URL : URL de la base de données (optionnel)
```

5. Initialiser la base de données :
```bash
flask db upgrade
```

6. Créer le premier compte administrateur :
```bash
python scripts/create_admin.py admin@example.com motdepasse
```

## Lancement

1. Démarrer l'application :
```bash
python run.py
```

2. Accéder à l'application dans votre navigateur :
```
http://localhost:5000
```

## Structure du projet

```
simulation-parlementaire/
├── app/
│   ├── models/          # Modèles de données
│   ├── routes/          # Routes de l'application
│   ├── static/          # Fichiers statiques (CSS, JS)
│   ├── templates/       # Templates HTML
│   ├── utils/          # Utilitaires
│   ├── tests/          # Tests unitaires
│   └── __init__.py     # Configuration de l'application
├── migrations/         # Migrations de la base de données
├── scripts/           # Scripts utilitaires
│   └── create_admin.py # Script de création du premier administrateur
├── requirements.txt    # Dépendances Python
├── run.py             # Point d'entrée de l'application
└── README.md          # Documentation
```

## Gestion des droits

### Création du premier administrateur

Lors du premier lancement de l'application, il est nécessaire de créer un compte administrateur. Utilisez le script fourni :

```bash
python scripts/create_admin.py email@example.com motdepasse
```

### Attribution des rôles

- Les nouveaux comptes sont créés sans rôle par défaut
- Seuls les administrateurs peuvent attribuer des rôles aux utilisateurs
- Les rôles sont attribués via l'interface d'administration

## Rôles utilisateurs

- **Député** : 
  - Proposer des amendements
  - Voter sur les textes et amendements
  - Consulter les documents législatifs

- **Rapporteur** : 
  - Gérer les textes en commission
  - Proposer des rapports
  - Modérer les amendements

- **Secrétaire** :
  - Gérer l'ordre du jour
  - Enregistrer les votes
  - Publier les documents officiels

- **Chef de groupe** :
  - Coordonner les positions du groupe
  - Représenter le groupe en séance
  - Gérer les amendements du groupe

- **Représentant d'intérêt** :
  - Proposer des amendements
  - Participer aux consultations
  - Suivre les débats

- **Rapporteur fictif** :
  - Simuler le rôle de rapporteur
  - Proposer des rapports fictifs
  - Participer aux débats

- **Administrateur** : 
  - Gérer les utilisateurs et leurs rôles
  - Configurer le système
  - Superviser l'ensemble du processus

## Tests

Pour exécuter les tests :
```bash
pytest
```

Pour la couverture de code :
```bash
coverage run -m pytest
coverage report
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence EULA de la SPECQUE. Voir le fichier `EULA.md` pour plus de détails. Cette licence vous permet de :
- Modifier le code source
- Partager l'application
- Distribuer vos modifications
- Adapter l'application à vos besoins

Pour toute question concernant la licence, veuillez consulter le fichier `EULA.md` ou contacter la SPECQUE. 