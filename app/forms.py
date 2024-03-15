from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sqlA
from app import db
from app.models import User

class LoginForm(FlaskForm):
    # DataRequired validator just validates field is not empty
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
    
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()]) # Email() ensures input matches input of an actual email
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")]) # EqualTo() does what you'd expect
    submit = SubmitField("Register")
    
    # WTForms will invoke these in addition to stock validators, true for any function with name validate_<name>
    def validate_username(self, username):
        user = db.session.scalar(sqlA.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError("Username Taken! Please try something else.")
        
    def validate_email(self, email):
        user = db.session.scalar(sqlA.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError("Email already used! Please use a different email address.")