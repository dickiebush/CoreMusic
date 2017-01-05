from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, IntegerField, SelectField
from wtforms import validators 

class SignupForm(FlaskForm):
    email  = StringField('Email:', validators=[validators.DataRequired("A valid email is required"), validators.email("A valid email is required")])
    name   = StringField('Full Name:', validators=[validators.DataRequired("Your full name is required")])
    number = StringField('Phone Number:', validators=[validators.DataRequired("A valid 10-digit phone number is required"), \
                         validators.Length(10,10,"Please enter a 10 digit phone number"), \
                         validators.Regexp('[0-9]{10}')])
    artists = TextAreaField('Enter your favorite music artists, separated by commas', validators=[validators.DataRequired("Please enter your favorite artists")])
    password = PasswordField('Password:', validators=[validators.Length(6,15,"Password must be six or more characters")])
    submit = SubmitField("Subscribe")

class LoginForm(FlaskForm):
    email  = StringField('Email:', validators=[validators.DataRequired("A valid email is required"), validators.email("A valid email is required")])
    passowrd = password = PasswordField('Password:', validators=[validators.Length(6,15,"Password must be six or more characters")])
    remember_me = BooleanField('Remember Me', default=True)
    submit = SubmitField("Log in")
