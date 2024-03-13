from flask import render_template
from app import app

# Decorators which define the app route, both decorate the index function
@app.route("/api/v1")
def apiV1():
    return "This will do something at some point I hope"

@app.route("/index")
def index():
    user = {"username": "matthew"}
    # uses the Jinja template engine that comes with flask
    return render_template("index.html", user=user)