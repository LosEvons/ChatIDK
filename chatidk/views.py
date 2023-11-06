from chatidk import get_db
db = get_db() # Declare database
from flask import Blueprint, render_template, request, session, redirect, flash

main = Blueprint("main", __name__)
@main.route("/")
def index():
    return render_template("index.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        msg = None
        
        if not username:
            msg = "Username is required!"
        elif not password:
            msg = "Password is required!"
            
        if msg is None:
            err = db.login(username, password)
            if not err:
                session["username"] = username
                flash("Logged in!")
                return redirect("/")
            else:
                msg = err
        
        flash(msg)
    
    return render_template("login.html")

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        msg = None
        
        if not username:
            msg = "Username is required!"
        elif not password:
            msg = "Password is required!"
            
        if msg is None:
            err = db.register(username, password)
            if not err:
                session["username"] = username
                flash("Account created!")
                return redirect("/")
            else:
                msg = err
        
        flash(msg)
    
    return render_template("register.html")

@main.route("/logout", methods=["GET"])
def logout():
    del session["username"]
    flash("Logged out!")
    return redirect("/")

@main.route("/deactivate", methods=["GET"])
def deactivate():
    msg = None
    err = db.deactivate_user(session["username"])
    if not err:
        del session["username"]
        msg = "Account deactivated!"
    else:
        msg = err
    
    flash(msg) 
            
    return redirect("/")