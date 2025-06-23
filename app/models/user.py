from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=True)  # 'deputy', 'reporter', 'secretary', 'group_leader', 'interest_representative', 'fictive_reporter', 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    amendments = db.relationship('Amendment', backref='author', lazy=True)
    votes = db.relationship('Vote', backref='voter', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_deputy(self):
        return self.role == 'deputy'

    def is_reporter(self):
        return self.role == 'reporter'

    def is_secretary(self):
        return self.role == 'secretary'

    def is_group_leader(self):
        return self.role == 'group_leader'

    def is_interest_representative(self):
        return self.role == 'interest_representative'

    def is_fictive_reporter(self):
        return self.role == 'fictive_reporter'

    def get_role_display_name(self):
        role_names = {
            'admin': 'Administrateur',
            'deputy': 'Député',
            'reporter': 'Rapporteur',
            'secretary': 'Secrétaire',
            'group_leader': 'Chef de groupe',
            'interest_representative': 'Représentant d\'intérêt',
            'fictive_reporter': 'Rapporteur fictif'
        }
        return role_names.get(self.role, 'Non défini')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 