from chatidk import get_engine
ngin = get_engine() # Declare engine
from flask import Blueprint, g, render_template, request, session, redirect, flash

main = Blueprint("main", __name__)
@main.route("/")
def index():
    return render_template("home.html")

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
            err = ngin.um.login(username, password)
            if not err:
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
            err = ngin.um.register(username, password)
            if not err:
                flash("Account created!")
                return redirect("/")
            else:
                msg = err
        
        flash(msg)
    
    return render_template("register.html")

@main.route("/logout", methods=["GET"])
def logout():
    ngin.um.logout()
    flash("Logged out!")
    return redirect("/")

@main.route("/deactivate", methods=["GET"])
def deactivate():
    msg = None
    err = ngin.um.deactivate_user()
    if not err:
        ngin.um.logout()
        msg = "Account deactivated!"
    else:
        msg = err
    
    flash(msg) 
            
    return redirect("/")

@main.route("/chat")
def chat():
    print(request.form["user"])
    

# VARIABLE INJECTIONS
@main.context_processor
def inject_users():
    return dict(users=ngin.um.get_other_users())

@main.context_processor
def inject_active_user():
    return dict(active_user=ngin.um.au)