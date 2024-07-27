# ThrowbackCalendar

This is a simple calendar that allows you to save events you want to remember. They will be shown every year on the given date.

## Setup

    git clone https://github.com/schneidr/ThrowbackCalendar
    cd ThrowbackCalendar
    python3 -m virtualenv .
    . bin/activate
    pip install -r requirements.txt

### Setup production instance

    # inside the virtualenv
    pip install gunicorn
    # configure gunicorn to be run by your service manager
    gunicorn -w 4 ThrowbackCalendar:app
    # configure your reverse proxy

### Start development environment

    flask --app ThrowbackCalendar run --debug

## Components

- Flask https://flask.palletsprojects.com/en/3.0.x/
