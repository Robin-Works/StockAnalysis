from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sqlA
from app import db
from app.models import User
from urllib.parse import urlsplit
from app.stocks import fetchSPData, fetchTrendData

# Decorator which defines the api I would like to implement for my app
@app.route("/api/v1/stonks")
def apiV1():
    companies = fetchSPData()
    
    # currently, pytrends is broken so this won't work :(
    # trendsDict = fetchTrendData(companies)
    return companies.to_dict()

# Index route renders index.html with a test post
@app.route("/index")
@login_required
def index():
    posts = [
        {
            "author": {"username": current_user.username},
            "body": "I am in Wisconsin :("
        }
    ]
    # uses the Jinja template engine that comes with flask
    return render_template("index.html", title="Home Page", posts=posts)

# Register is the endpoint for becoming a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    # Return to index if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    # Create registration form
    form = RegistrationForm()
    
    # If a POST request is sent
    if form.validate_on_submit():
        # Create new user from form input data
        user = User(username=form.username.data, email=form.email.data)
        user.setPassword(form.password.data)
        
        # Add new user to db, double buffer type deal
        db.session.add(user)
        db.session.commit()
        
        flash("Congratulations, {}, you are now registered!".format(user.username))
        
        # Redirect to /login endpoint
        return redirect(url_for("login"))
    
    # Display register page for GET request
    return render_template("register.html", title="Register", form=form)

# login endpoint defines the front end for logging in
@app.route("/login", methods=['GET', 'POST'])
def login():
    # If user is already authenticated, go to index endpoint
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    # Create login form
    form = LoginForm()
    
    # form.validate_on_submit() will return false when GET request to page is sent
    if form.validate_on_submit():
        user = db.session.scalar(sqlA.select(User).where(User.username == form.username.data)) # returns user object if it exists
        
        # Check if user exists and if password is correct
        if user is None or not user.checkPassword(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        
        # Flask defined login functionality
        login_user(user, remember=form.remember.data)
        
        # find what the next page is if being redirected from a login_required route
        nextPage = request.args.get("next")
        if not nextPage or urlsplit(nextPage).netloc != "":
            nextPage = url_for("index")
        return redirect(nextPage)
    
    # passes form object to template with name form for GET request
    return render_template("login.html", title="Sign In", form=form)

# Endpoint defines user profile page
@app.route("/user/<username>")
@login_required
def user(username):
    # Grab first username field from DB or return 404
    user = db.first_or_404(sqlA.select(User).where(User.username == username))
    
    # Test posts to be displayed
    posts = [
        {"author": user, "body": "Test Post #1"},
        {"author": user, "body": "Test Post #2"}
    ]
    
    # Render user and post data
    return render_template("user.html", user=user, posts=posts)

# Endpoint defines user profile edit page
@app.route("/editProfile", methods=["GET", "POST"])
def editProfile():
    # Create edit profile form with the current_user's username
    form = EditProfileForm(current_user.username)
    
    # If POST request
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.aboutMe = form.aboutMe.data
        db.session.commit()
        flash("Your changes have been saved!")
        return redirect(url_for("editProfile"))
    elif request.method == "GET": # Autopopulate form data with current username and about me data for GET request
        form.username.data = current_user.username
        form.aboutMe.data = current_user.aboutMe
        
    # render edit profile form
    return render_template("editProfile.html", title="Edit Profile", form=form)

# Basic flask logout functionality endpoint
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))