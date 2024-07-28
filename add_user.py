#!/usr/bin/env python3

import bcrypt
import getpass
import sqlite3
import sys

email = input("Email: ")
password = getpass.getpass("Password: ")
password_repeated = getpass.getpass("Repeat password: ")
if password != password_repeated:
    sys.exit("Error: Passwords don't match")
hashed_password = bcrypt.hashpw(bytes(password, encoding="utf-8"), bcrypt.gensalt())

try:
    connection = sqlite3.connect("events.db")
    cursor = connection.cursor()
    cursor.execute(
        "REPLACE INTO users (email,password) VALUES (?,?)", (email, hashed_password)
    )
    connection.commit()
    print("User {0} added successfully.".format(email))
except Exception as e:
    print("Error: {0}".format(e))
