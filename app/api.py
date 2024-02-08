# This file contains most of logis and features
import platform
import uuid
from flask import request, jsonify
from app import app
from app.db import get_db

## devlopment tools: /dev/

# this is the first API endpoint, for test only, it will return a sample obj
@app.route("/dev/env")
def dev_env():
    return {
        "backend":"Flask",
        "os": platform.platform()
    }

## prod routes:

# this is the endpoint for open form registration
@app.route("/prod/openregistration",methods=["post"])
def open_registration():
    content = request.json
    first_name = content["firstName"]
    last_name = content["lastName"]
    phone = content["phone"]
    email = content["email"]
    status = content['status']
    department = content["department"]
    username = str(uuid.uuid4())
    password = ""
    db = get_db()
    error = None
    if not first_name:
        error = "first name not defined"
    elif not status:
        error = "student status not defined"
    if error is None:
        try:
            db.execute(
                "INSERT INTO user (username, password, first_name, last_name, phone, email, status, department) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (username, password, first_name, last_name, phone, email, status, department),
            )
            db.commit()
            return "OK"
        except db.IntegrityError:
            error = f"User {username} is already registered."
    return error

# this is the route to fetch the registered users from db
@app.route("/prod/fetchallusers",methods=["get"])
def fetch_all_users():
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute('SELECT * FROM user')
        res = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
        db.commit()
    except db.IntegrityError:
        error = f"db error"
        return error
    return jsonify(res)