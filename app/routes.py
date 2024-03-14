from flask import render_template, flash, redirect, url_for
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

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # form.validate_on_submit() will return false when GET request to page is sent
    if form.validate_on_submit():
        # flash function shows message for user (temp solution)
        flash("Login requested for user {}, remember={}".format(form.username.data, form.remember.data))
        return redirect(url_for("index"))
    # passes form object to template with name form
    return render_template("login.html", title="Sign In", form=form)