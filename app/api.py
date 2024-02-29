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
        "project": "blog-backend",
        "backend":"Flask",
        "os": platform.platform()
    }

## prod routes:

# this is the endpoint for open form registration
@app.router("/prod/registration", methods=("post"))
def user_registration():
    content = request.json
    username = content["username"]
    password = content["password"]
    name = content["name"]
    avatar = content["avatar"]
    if not username:
        return "username not defined"
    if not name:
        return "name not defined"
    try:
        db.execute("INSERT INTO user (username, password, name, avatar) VALUES (?,?,?,?)"), (username, password, name, avatar)
        db.commit()
        return "OK"
    except db.IntegrityError:
        return f"User {username} is already registered."
    
@app.router("/prod/addpost", methods=("post"))
def add_post():
    return "OK"


@app.route("/prod/openregistration",methods=["post"])
def open_registration():
    content = request.json
    name = content["name"]
    gender = content["gender"]
    # phone = content["phone"]
    email = content["email"]
    status = content['status']
    department = content["department"]
    consent = content["consent"]
    username = str(uuid.uuid4())
    password = ""
    db = get_db()
    error = None
    if not name:
        error = "name not defined"
    elif not status:
        error = "student status not defined"
    if error is None:
        try:
            db.execute(
                "INSERT INTO user (username, password, name, email, status, department, consent, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (username, password, name, email, status, department, consent, gender),
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