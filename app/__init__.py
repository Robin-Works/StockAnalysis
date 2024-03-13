from flask import Flask
from config import Config

# Routes need to import app so this is a dependency workaround
app = Flask(__name__)
app.config.from_object(Config)

from app import routes