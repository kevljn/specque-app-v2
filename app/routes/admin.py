from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.user import User
from app.forms import RoleAssignmentForm
from app import db

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Accès non autorisé.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/user/<int:user_id>/role', methods=['GET', 'POST'])
@login_required
@admin_required
def assign_role(user_id):
    user = User.query.get_or_404(user_id)
    form = RoleAssignmentForm()
    
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.commit()
        flash(f'Rôle attribué avec succès à {user.email}.', 'success')
        return redirect(url_for('admin.users'))
    
    # Pré-remplir le formulaire avec le rôle actuel
    if user.role:
        form.role.data = user.role
    
    return render_template('admin/assign_role.html', form=form, user=user) 