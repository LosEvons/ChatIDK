import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config, TestConfig

# Initialize app

app = Flask(__name__, instance_relative_config=True)

# Choose config
app.config.from_object(TestConfig if app.config["TESTING"] else Config)

# Make sure instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Initialize database
from .psql_db import CredentialManager
db = None
def get_db():
    global db
    if db is None:
        db = CredentialManager(SQLAlchemy(app))
    return db

# Import blueprints/views
from .views import main
app.register_blueprint(main)

# Run app
if __name__ == "__main__":
    app.run()