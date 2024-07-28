import bcrypt
from calendar import monthrange
from datetime import datetime
from flask import flash, Flask, Response
from flask import redirect, render_template, request, session, url_for
from flask_babel import Babel, gettext
import sqlite3
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
app.config.from_pyfile("settings.py")


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
cursor.execute(
    """
               CREATE TABLE IF NOT EXISTS events (
                date TEXT NOT NULL,
                name TEXT NOT NULL,
                url TEXT,
                parent_name TEXT,
                parent_url TEXT
               )
               """
)
cursor.execute(
    """
               CREATE TABLE IF NOT EXISTS users (
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
               )
               """
)


def add_event(date: str, name: str, url: str, parent_name: str, parent_url: str):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO events (date,name,url,parent_name,parent_url) VALUES (?,?,?,?,?)",
        (date, name, url, parent_name, parent_url),
    )
    connection.commit()


def update_event(
    id: int, date: str, name: str, url: str, parent_name: str, parent_url: str
):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE events SET date=?,name=?,url=?,parent_name=?,parent_url=? WHERE rowid=?",
        (date, name, url, parent_name, parent_url, id),
    )
    connection.commit()


def delete_event(id: int):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM events WHERE rowid=?",
        (id,),
    )
    connection.commit()


def get_events(month: str) -> dict:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT rowid,strftime('%d', `date`) AS day,strftime('%Y', `date`) AS year,name,url,parent_name,parent_url FROM events WHERE date LIKE ?",
        ("%-" + month + "-%",),
    )
    results = cursor.fetchall()
    events = {}
    for item in results:
        event = {
            "id": int(item[0]),
            "day": int(item[1]),
            "year": int(item[2]),
            "name": item[3],
            "url": item[4],
            "parent_name": item[5],
            "parent_url": item[6],
        }
        if not event["day"] in events:
            events[event["day"]] = {}
        if not event["year"] in events[event["day"]]:
            events[event["day"]][event["year"]] = []
        events[event["day"]][event["year"]].append(event)
    return events


def validate_user(email: str, password: str) -> bool:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT email,password FROM users WHERE email=?",
        (email,),
    )
    user = cursor.fetchone()
    if user == None:
        return False
    hashed_password = str(user[1]).encode("utf-8")
    return bcrypt.hashpw(password.encode("utf-8"), hashed_password) == hashed_password


@app.route("/")
def index():
    if "user_email" not in session:
        return redirect(url_for("login"))
    now = datetime.now()
    return redirect(url_for("show_month", month=now.month))


@app.route("/<int:month>", methods=["GET", "POST"])
def show_month(month: int):
    if "user_email" not in session:
        session["previous_url"] = url_for("show_month", month=month)
        return redirect(url_for("login"))
    if month > 12:
        return redirect(url_for("show_month", month=1))
    if month < 1:
        return redirect(url_for("show_month", month=12))
    now = datetime.now()
    current_month = datetime.now()
    if month != 0:
        current_month = datetime(current_month.year, month, current_month.day)
    if request.method == "POST":
        date = "{0:04d}-{1:02d}-{2:02d}".format(
            int(request.form["year"]),
            int(request.form["month"]),
            int(request.form["day"]),
        )
        if request.form["id"] == "":
            add_event(
                date,
                request.form["name"],
                request.form["url"],
                request.form["parent_name"],
                request.form["parent_url"],
            )
        else:
            if request.form["action"] == "delete":
                delete_event(int(request.form["id"]))
            else:
                update_event(
                    int(request.form["id"]),
                    date,
                    request.form["name"],
                    request.form["url"],
                    request.form["parent_name"],
                    request.form["parent_url"],
                )
    events = get_events("{0:02d}".format(current_month.month))
    days_in_month = monthrange(current_month.year, current_month.month)
    if current_month.month == 2:
        days_in_month = (3, 29)
    return render_template(
        "index.html",
        now=now,
        current_month=current_month,
        days_in_month=days_in_month[1],
        month_names=month_names,
        events=events,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if validate_user(request.form.get("email"), request.form.get("password")):
            session["user_email"] = request.form.get("email")
            if "previous_url" in session:
                previous_url = session["previous_url"]
                del session["previous_url"]
                return redirect(previous_url)
            return redirect(url_for("index"))
    return render_template("login.html", email=request.form.get("email"))


@app.errorhandler(401)
def page_not_found(error):
    return render_template("unauthorized.html"), 401


@app.errorhandler(404)
def page_not_found(error):
    return "Not found", 404


@app.template_filter("monthname")
def monthname_filter(s):
    return gettext(month_names[s])
