# ThrowbackCalendar

This is a simple calendar that allows you to save events you want to remember. They will be shown every year on the given date.

## Setup

    git clone https://github.com/schneidr/ThrowbackCalendar
    cd ThrowbackCalendar
    python3 -m virtualenv .
    . bin/activate
    pip install -r requirements.txt

Copy `settings-example.py` to `settings.py` and set a secret in the `SECRET_KEY` variable. You can create a secret by running:

    python -c 'import secrets; print(secrets.token_hex())'

### Setup production instance

    # inside the virtualenv
    pip install gunicorn
    # configure gunicorn to be run by your service manager
    gunicorn -w 4 ThrowbackCalendar:app
    # configure your reverse proxy

### Start development environment

    flask --app ThrowbackCalendar run --debug

## Add user

Make sure you've started the application at least once, so the tables have been created.

    $ ./add_user.py
    Email: name@example.com
    Password: 
    User name@example.com added successfully.

The password will not be printed.

Now you can log in with the user on the application.

## Components

- Flask https://flask.palletsprojects.com/en/3.0.x/
