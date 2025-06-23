from flask import render_template, jsonify, request
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request_error(error):
        if request_wants_json():
            return jsonify(error=str(error)), 400
        return render_template('errors/400.html'), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        if request_wants_json():
            return jsonify(error=str(error)), 401
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        if request_wants_json():
            return jsonify(error=str(error)), 403
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        if request_wants_json():
            return jsonify(error=str(error)), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        if request_wants_json():
            return jsonify(error=str(error)), 500
        return render_template('errors/500.html'), 500

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        if isinstance(error, HTTPException):
            return error
        app.logger.error('Unhandled Exception: %s', str(error))
        if request_wants_json():
            return jsonify(error='Internal Server Error'), 500
        return render_template('errors/500.html'), 500

def request_wants_json():
    return request.accept_mimetypes.accept_json and \
           not request.accept_mimetypes.accept_html 