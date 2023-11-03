from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from markupsafe import escape

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<p_choice>")
def choice(p_choice):
    e_choice = escape(p_choice)
    match e_choice:
        case "chose_login":
            return render_template("index.html", chose_login=True)
        case "chose_register":
            return render_template("index.html", chose_register=True)
        case _:
            return redirect("/")

@app.route("/<name>", methods=["GET", "POST"])
def login(name):
    escape_name = escape(name)
    if escape_name == "login":
        username = request.form["username"]
        password = request.form["password"]
        sql = text("SELECT id, password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            return render_template("index.html", chose_login=True, lerrmsg="Bad username!")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = username
                return redirect("/")
            else:
                return render_template("index.html", chose_login=True, lerrmsg="Bad password!")

    elif escape_name == "register":
        username = request.form["username"]
        password = request.form["password"]
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        session["username"] = username
        return render_template("index.html", logmsg="New account created!")
        
        
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")