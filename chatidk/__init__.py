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

# Initialize app
from chatidk.engine.engine import Engine
ngin = None
def get_engine():
    global ngin
    if ngin is None:
        ngin = Engine(SQLAlchemy(app), app.config["UPLOAD_FOLDER"])
    return ngin

# Import blueprints/views
from .views import main
app.register_blueprint(main)

# Run app
if __name__ == "__main__":
    app.run()