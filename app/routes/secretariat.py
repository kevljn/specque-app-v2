from flask import Blueprint, render_template, request, jsonify, abort, flash
from flask_login import login_required, current_user
from app.models.legislative import Amendment
from app import db

secretariat_bp = Blueprint('secretariat', __name__)

@secretariat_bp.route('/amendments')
@login_required
def amendments():
    if not current_user.is_secretariat():
        flash('Accès refusé : seuls les membres du secrétariat peuvent accéder à cette page.', 'error')
        abort(403)
    amendments = Amendment.query.order_by(Amendment.order.asc().nullslast(), Amendment.id.asc()).all()
    return render_template('secretariat/amendments.html', amendments=amendments)

@secretariat_bp.route('/amendments/reorder', methods=['POST'])
@login_required
def reorder_amendments():
    if not current_user.is_secretariat():
        flash('Accès refusé : seuls les membres du secrétariat peuvent accéder à cette page.', 'error')
        abort(403)
    data = request.get_json()
    for i, amend_id in enumerate(data['order']):
        amend = Amendment.query.get(int(amend_id))
        if amend:
            amend.order = i + 1
    db.session.commit()
    flash('Ordre des amendements mis à jour.', 'success')
    return jsonify({'status': 'success'}) 