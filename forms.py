from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, SelectField
from wtforms import validators 

class SignupForm(FlaskForm):
    email  = StringField('Email', validators=[validators.DataRequired(), validators.email()])
    name   = StringField('Name', validators=[validators.DataRequired("Please enter your name")])
    number = StringField('Phone Number', validators=[validators.DataRequired("Please enter your phone number"), \
                         validators.Length(10,10,"Please enter a 10 digit phone number"), \
                         validators.Regexp('[0-9]{10}')])
    artists = StringField('Enter your 5 favorite music artists, separated by commas', validators=[validators.DataRequired("Please enter your favorite artists")])
    submit = SubmitField("Sign up")


