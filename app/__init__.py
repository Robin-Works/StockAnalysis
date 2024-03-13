from flask import Flask

# Routes need to import app so this is a dependency workaround
app = Flask(__name__)

from app import routes