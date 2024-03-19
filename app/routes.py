from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sqlA
from app import db
from app.models import User
from urllib.parse import urlsplit

# Decorators which define the app route, both decorate the index function
@app.route("/api/v1")
def apiV1():
    return "This will do something at some point I hope"

@app.route("/index")
@login_required
def index():
    posts = [
        {
            "author": {"username": "Matthew"},
            "body": "I am in Wisconsin :("
        }
    ]
    # uses the Jinja template engine that comes with flask
    return render_template("index.html", title="Home Page", posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create new user from form input data
        user = User(username=form.username.data, email=form.email.data)
        user.setPassword(form.password.data)
        
        # Add new user to db, double buffer type deal
        db.session.add(user)
        db.session.commit()
        
        flash("Congratulations, {}, you are now registered!".format(user.username))
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    # form.validate_on_submit() will return false when GET request to page is sent
    if form.validate_on_submit():
        user = db.session.scalar(sqlA.select(User).where(User.username == form.username.data)) # returns user object if it exists
        if user is None or not user.checkPassword(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember.data)
        
        # find what the next page is if being redirected from a login_required route
        nextPage = request.args.get("next")
        if not nextPage or urlsplit(nextPage).netloc != "":
            nextPage = url_for("index")
        return redirect(nextPage)
    # passes form object to template with name form
    return render_template("login.html", title="Sign In", form=form)

@app.route("/user/<username>")
@login_required
def user(username):
    user = db.first_or_404(sqlA.select(User).where(User.username == username))
    posts = [
        {"author": user, "body": "Test Post #1"},
        {"author": user, "body": "Test Post #2"}
    ]
    return render_template("user.html", user=user, posts=posts)

@app.route("/editProfile", methods=["GET", "POST"])
def editProfile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.aboutMe = form.aboutMe.data
        db.session.commit()
        flash("Your changes have been saved!")
        return redirect(url_for("editProfile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.aboutMe.data = current_user.aboutMe
    return render_template("editProfile.html", title="Edit Profile", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))