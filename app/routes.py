from flask import render_template
from app import app
from app.forms import LoginForm

# Decorators which define the app route, both decorate the index function
@app.route("/api/v1")
def apiV1():
    return "This will do something at some point I hope"

@app.route("/index")
def index():
    user = {"username": "matthew"}
    # uses the Jinja template engine that comes with flask
    return render_template("index.html", user=user)

@app.route("/login")
def login():
    form = LoginForm()
    # passes form object to template with name form
    return render_template("login.html", title="Sign In", form=form)