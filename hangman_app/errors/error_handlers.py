from flask import render_template
from hangman_app import app

@app.errorhandler(400)
def handle_bad_request(error):
    return render_template('errors/400.html'), 400

@app.errorhandler(401)
def handle_unauthorized(error):
    return render_template('errors/401.html'), 401

@app.errorhandler(403)
def handle_forbidden(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def handle_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def handle_internal_server_error(error):
    return render_template('errors/500.html'), 500

