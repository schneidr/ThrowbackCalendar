#!/usr/bin/env python3

import bcrypt
import getpass
import sqlite3

email = input("Email: ")
password = getpass.getpass("Password: ")
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
