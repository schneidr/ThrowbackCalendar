from flask import flash, Flask, Response
from flask import redirect, render_template, request, session, url_for
from flask_babel import Babel, gettext

app = Flask(__name__)
# app.config.from_pyfile('settings.cfg')
# app.secret_key = app.config['SECRET_KEY']
babel = Babel(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.errorhandler(401)
def page_not_found(error):
    return render_template('unauthorized.html'), 401

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
