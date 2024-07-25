from calendar import monthrange
from datetime import datetime
from flask import flash, Flask, Response
from flask import redirect, render_template, request, session, url_for
from flask_babel import Babel, gettext

app = Flask(__name__)
# app.config.from_pyfile('settings.cfg')
# app.secret_key = app.config['SECRET_KEY']

def get_locale():
    return request.accept_languages.best_match(['de', 'en'])

babel = Babel(app, locale_selector=get_locale)

month_names=[
    'dummy',
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
]


def render_calendar(month: int = 0):
    now = datetime.now()
    current_month = datetime.now()
    if month != 0:
        current_month = datetime(current_month.year,
                       month,
                       current_month.day)
    days_in_month = monthrange(current_month.year, current_month.month)
    return render_template(
        'index.html',
        now=now,
        current_month=current_month,
        days_in_month=days_in_month[1],
        month_names=month_names
    )


@app.route("/")
def index():
    return render_calendar(0)

@app.route("/<int:month>")
def show_month(month: int):
    if month > 12:
        return redirect(url_for('show_month', month=1))
    if month < 1:
        return redirect(url_for('show_month', month=12))
    return render_calendar(month)

@app.errorhandler(401)
def page_not_found(error):
    return render_template('unauthorized.html'), 401

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.template_filter('monthname')
def monthname_filter(s):
    return gettext(month_names[s])