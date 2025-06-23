from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.legislative import LegislativeText
from app.models.user import User
import app.models.legislative  # Pour injecter is_secretariat sur User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    texts = LegislativeText.query.all()
    return render_template('main/dashboard.html', texts=texts) 