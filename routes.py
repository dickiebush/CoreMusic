from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Song, User
import os
from forms import SignupForm, LoginForm
import requests
from celery import Celery
from twilio.rest import TwilioRestClient as TRC
# link to database used for heroku 
# DATABASE_URL=$(heroku config:get DATABASE_URL -a coremusic)

# magical incantations 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL']
app.config['CELERY_RESULT_BACKEND'] = os.environ['REDIS_URL']

celery= Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
 
app.secret_key = "development_key"

db.init_app(app)

# initialize tables 
with app.app_context():
    db.create_all()
    db.session.commit()


@app.route("/")
def index():

    # if user is logged in send to home page
    if 'number' in session:
        return(redirect(url_for('home')))

    return(render_template("index.html"))
    #return(render_template("index.html"))

@app.route("/signup", methods=['GET','POST'])
def signup():
    form = SignupForm()

    # if user is logged in, go to home page 
    if 'number' in session:
        return redirect(url_for("home"))

    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html', form=form)
        else: 
            user = User(form.email.data.lower(), form.name.data.title(), form.number.data, form.artists.data.title(), form.password.data)
            # text me that a new user signed up somehow asynchronously 
            new_user_text_me.delay(user.name, user.email, user.number, user.artists)
            welcome_new_user.delay(user.name, user.number)
            with app.app_context():
                db.session.add(user)
                db.session.commit()

            session['number'] = user.number
            return redirect(url_for('welcome'))
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    # if user is logged in, go to homepage
    if 'number' in session:
        return redirect(url_for("home"))

    form = LoginForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            # create session
            session['number'] = form.number.data
            # send them to home page
            return(redirect(url_for('home')))
    return render_template("login.html", form=form)
    #login gonna be required 
    # let them alter their information 

@app.route("/home")
def home():

    if 'number' not in session:
        return redirect(url_for("login"))

    return("<a href=\"/logout\" class=\"btn btn-default btn-primary navbar-btn\" style=\"font-size:17px\">Log out</a>")

@app.route("/logout")
def logout():

    # if not logged in cant log out
    if 'number' not in session:
        return redirect(url_for("login"))

    session.pop('number', None)

    return(redirect(url_for('login')))

# handle that you cant access this without being logged in 
@app.route("/welcome")
def welcome():
    return(render_template('welcome.html'))

@app.route("/aboutus")
def aboutus():
    return(render_template("aboutus.html"))


@app.route("/settings")
def settings():
    pass
###########################################################################

@celery.task
def new_user_text_me(name, email, number, artists):
    client = twilio_client()
    twilio_number = "+18133363411"

    body = "{} just signed up. Their number is {}. Their email is {}. He likes {}".format(name, number, email, artists)
    
    # send text message currently to me only 
    client.messages.create(to = "+18139095372", from_ = twilio_number, body = body)

@celery.task
def welcome_new_user(name, number):
    client = twilio_client()
    twilio_number = "+18133363411"

    body = "Hey {}! Welcome to Core Music. Via SMS, we'll send you direct links to every new song one of your favorite artists drops. Enjoy!".format(name.split()[0])

    client.messages.create(to = number, from_ = twilio_number, body = body)


    body = "Also, the links we send open Spotify, Soundcloud, and YouTube directly on your phone. Make sure you have these downloaded or else they won't work!"
    client.messages.create(to = number, from_ = twilio_number, body = body)
def twilio_client():
    account_sid   = "AC79432a906b5df034fa4604d80dee6079"
    auth_token    = "077422f1a2129d43670ca8b802cef484"
    return TRC(account_sid, auth_token)

if __name__ == "__main__":
    app.run(debug=True)