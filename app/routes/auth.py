from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db
from app.forms import RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email déjà utilisé.', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(
            email=form.email.data,
            role=None  # Pas de rôle par défaut
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Inscription réussie ! Vous pouvez vous connecter.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Connexion réussie.', 'success')
            next_page = request.args.get('next')
            
            # Redirection basée sur le rôle
            if user.is_admin():
                return redirect(next_page or url_for('admin.dashboard'))
            elif user.is_secretary():
                return redirect(next_page or url_for('secretariat.dashboard'))
            else:
                return redirect(next_page or url_for('main.dashboard'))
        
        flash('Email ou mot de passe incorrect.', 'error')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous êtes déconnecté.', 'info')
    return redirect(url_for('main.dashboard')) 