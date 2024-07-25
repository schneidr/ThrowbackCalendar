from calendar import monthrange
from datetime import datetime
from flask import flash, Flask, Response
from flask import redirect, render_template, request, session, url_for
from flask_babel import Babel, gettext
import sqlite3

app = Flask(__name__)
# app.config.from_pyfile('settings.cfg')
# app.secret_key = app.config['SECRET_KEY']


def get_locale():
    return request.accept_languages.best_match(["de", "en"])


babel = Babel(app, locale_selector=get_locale)

month_names = [
    "dummy",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
db_path = "events.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS events (
                date TEXT NOT NULL,
                name TEXT NOT NULL,
                url TEXT,
                description TEXT
               )
               """)


def add_event(date: str, name: str, url: str, description: str):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO events (date,name,url,description) VALUES (?,?,?,?)",
        (date, name, url, description)
    )
    connection.commit()


def get_events(month: str) -> dict:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT strftime('%d', `date`) AS day,strftime('%Y', `date`) AS year,name,url,description FROM events WHERE date LIKE ?",
        ("%-"+month+"-%",)
    )
    results = cursor.fetchall()
    events = {}
    for item in results:
        event = {
            "day": item[0],
            "year": item[1],
            "name": item[2],
            "url": item[3],
            "description": item[4]
        }
        if not event["day"] in events:
            events[event["day"]] = {}
        if not event["year"] in events[event["day"]]:
            events[event["day"]][event["year"]] = []
        events[event["day"]][event["year"]].append(event)
    return events
        


@app.route("/")
def index():
    now = datetime.now()
    return redirect(url_for("show_month", month=now.month))


@app.route("/<int:month>", methods = ["GET", "POST"])
def show_month(month: int):
    if month > 12:
        return redirect(url_for("show_month", month=1))
    if month < 1:
        return redirect(url_for("show_month", month=12))
    now = datetime.now()
    current_month = datetime.now()
    if month != 0:
        current_month = datetime(current_month.year, month, current_month.day)
    if request.method == 'POST':
        date = "{0:04d}-{1:02d}-{2:02d}".format(int(request.form["year"]), int(request.form["month"]), int(request.form["day"]))
        add_event(date, request.form["name"], request.form["url"], request.form["description"])
    events = get_events("{0:02d}".format(current_month.month))
    days_in_month = monthrange(current_month.year, current_month.month)
    return render_template(
        "index.html",
        now=now,
        current_month=current_month,
        days_in_month=days_in_month[1],
        month_names=month_names,
        events=events
    )


@app.errorhandler(401)
def page_not_found(error):
    return render_template("unauthorized.html"), 401


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


@app.template_filter("monthname")
def monthname_filter(s):
    return gettext(month_names[s])
