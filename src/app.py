from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from markupsafe import escape

from credential_manager import CredentialManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
credential_manager = CredentialManager(SQLAlchemy(app))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<p_state>")
def check_state(p_state):
    state = escape(p_state)
    match state:
        case "state_login":
            return render_template("index.html", state_login=True)
        case "state_register":
            return render_template("index.html", state_register=True)
        case _:
            return redirect("/")

@app.route("/<name>", methods=["GET", "POST"])
def login(name):
    username = request.form["username"]
    password = request.form["password"]
    escape_name = escape(name)
    if escape_name == "login":
        result_msg = credential_manager.login(username, password)
        if not result_msg:
            session["username"] = username
            return redirect("/")
        else:
            return render_template("index.html", state_login=True, logmsg=result_msg)

    elif escape_name == "register":
        result_msg = credential_manager.register(username, password)
        return render_template("index.html", logmsg=result_msg) 
        
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/deactivate")
def deactivate():
    result_msg = credential_manager.deactivate_user(session["username"])
    del session["username"]
    return render_template("index.html", logmsg=result_msg)