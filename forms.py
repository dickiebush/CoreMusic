from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, IntegerField, SelectField
from wtforms import validators 
from models import User

class SignupForm(FlaskForm):
    email  = StringField('Email:', validators=[validators.DataRequired("A valid email is required"), validators.email("A valid email is required")])
    name   = StringField('Full Name:', validators=[validators.DataRequired("Your full name is required")])
    number = StringField('Phone Number:', validators=[validators.DataRequired("A valid 10-digit phone number is required"), \
                         validators.Length(10,10,"Please enter a 10 digit phone number"), \
                         validators.Regexp('[0-9]{10}')])
    artists = TextAreaField('Enter your favorite music artists, separated by commas', validators=[validators.DataRequired("Please enter your favorite artists")])
    password = PasswordField('Password:', validators=[validators.Length(6,15,"Password must be six or more characters")])
    submit = SubmitField("Subscribe")


    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False;

        # first check if there is a person with the same phone number 
        user = User.query.filter_by(number=self.number.data).first()

        if user is not None:
            self.number.errors.append("This number is already subscribed. Log in below")
            return False
        else:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                self.email.errors.append("This email is already subscribed. Log in below")
                return False

        # made it through
        return True
class LoginForm(FlaskForm):
    number  = StringField('Phone number:', validators=[validators.DataRequired("A valid 10 digit phone number is required")])
    password = PasswordField('Password:', validators=[validators.DataRequired("Please enter your password")])
    remember_me = BooleanField('Remember me', default=True)
    submit = SubmitField("Log in")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False;

        user = User.query.filter_by(number=self.number.data).first()
        if user is None:
            self.number.errors.append("Phone number is not subscribed")
            return False
        else:
        # make more secure
            if user.password != self.password.data:
                self.password.errors.append("Invalid password. Please try again")
                return False

        # made it through
        return True
