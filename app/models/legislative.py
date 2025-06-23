from app import db
from datetime import datetime

class LegislativeText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, in_commission, in_plenary, adopted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    amendments = db.relationship('Amendment', backref='legislative_text', lazy=True)
    votes = db.relationship('Vote', backref='legislative_text', lazy=True)

class Amendment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    legislative_text_id = db.Column(db.Integer, db.ForeignKey('legislative_text.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='proposed')  # proposed, adopted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paragraph_index = db.Column(db.Integer, nullable=True)  # Index du paragraphe concerné
    type = db.Column(db.String(20), default='edit')  # edit, delete, add
    origin = db.Column(db.String(100), nullable=True)  # auteur, groupe, commission, compromis, etc.
    order = db.Column(db.Integer, nullable=True)  # pour le tri manuel
    legal_element_id = db.Column(db.Integer, db.ForeignKey('legal_element.id'), nullable=True)  # Nouvel indexage
    
    # Relations
    votes = db.relationship('Vote', backref='amendment', lazy=True)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    legislative_text_id = db.Column(db.Integer, db.ForeignKey('legislative_text.id'), nullable=False)
    amendment_id = db.Column(db.Integer, db.ForeignKey('amendment.id'), nullable=True)
    vote_type = db.Column(db.String(20), nullable=False)  # for, against, abstention
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 

# Ajout méthode is_secretariat au modèle User
from app.models.user import User

def is_secretariat(self):
    return self.role == 'secretariat'
User.is_secretariat = is_secretariat 

class LegalElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    legislative_text_id = db.Column(db.Integer, db.ForeignKey('legislative_text.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('legal_element.id'), nullable=True)
    type = db.Column(db.String(20), nullable=False)  # e.g. 'titre', 'preambule', 'dispositif', 'annexe', 'article', 'paragraphe', 'alinea', 'point', etc.
    index = db.Column(db.String(20), nullable=True)  # e.g. '1', 'I', 'A', 'a)', '1)', etc.
    title = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text, nullable=True)
    children = db.relationship('LegalElement', backref=db.backref('parent', remote_side=[id]), lazy=True) 