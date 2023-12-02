import os
from chatidk import get_engine
ngin = get_engine() # Declare engine
from flask import Blueprint, render_template, request, send_from_directory, redirect, flash, current_app
from werkzeug.utils import secure_filename

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

@main.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        target_name = request.args.get("chat")
        target_user = ngin.um.get_user(target_name)
        ngin.cm.ac = ngin.cm.get_chat(ngin.um.au, target_user)
    
    elif request.method == "POST":
        text = request.form["message"]
        ngin.cm.mm.add_message(ngin.um.au.id, ngin.cm.ac.id, text)
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.root_path, ngin.uf, filename)
            file.save(filepath)
            ngin.cm.mm.add_message_attachment(ngin.um.au.id, ngin.cm.ac.id, ngin.uf + "/" + filename)
    
    return render_template("chat.html")

@main.route("/download/<path:filename>", methods=["GET", "POST"])
def download(filename):
    return send_from_directory(current_app.root_path, filename)
    
    

# VARIABLE INJECTIONS
@main.context_processor
def inject_users():
    return dict(users=ngin.um.get_other_users())

@main.context_processor
def inject_active_user():
    return dict(active_user=ngin.um.au)

@main.context_processor
def inject_chat():
    return dict(chat=ngin.cm)