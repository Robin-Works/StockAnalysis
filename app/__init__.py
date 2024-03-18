from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Routes need to import app so this is a dependency workaround
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) # database engine oject associated with the app
migrate = Migrate(app, db) # migrate engine associated with the app
login = LoginManager(app)
login.login_view = "login" # specifies endpoint for logging in

from app import routes, models, errors