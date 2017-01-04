from flask import Flask, render_template, request, redirect, url_for
from models import db, Song, User
import os
from forms import SignupForm
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

with app.app_context():
    db.create_all()
    db.session.commit()

#from models import Song
@app.route("/")
def index():
    return redirect(url_for('signup'))

@app.route("/signup", methods=['GET','POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('signup.html', form=form)
        else: 
            user = User(form.email.data.lower(), form.name.data.title(), form.number.data, form.artists.data.title())
            # text me that a new user signed up somehow asynchronously 
            new_user_text_me.delay(user)

            with app.app_context():
                db.session.add(user)
                db.session.commit()

            return redirect(url_for('welcome'))
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

# handle that you cant access this without being logged in 
@app.route("/welcome")
def welcome():
    return(render_template('welcome.html'))

@celery.task
def welcome_new_user(user):
    client = twilio_client()
    twilio_number = "+18133363411"

    print("texting you about the new user")
    body = "{} just signed up. Their number is {}. Their email is {}".format(user.name, user.number, user.email)
    
    # send text message currently to me only 
    client.messages.create(to = "+18139095372", from_ = twilio_number, body = body)

@celery.task
def new_user_text_me(user):
    pass

def twilio_client():
    account_sid   = "AC79432a906b5df034fa4604d80dee6079"
    auth_token    = "077422f1a2129d43670ca8b802cef484"
    return TRC(account_sid, auth_token)


if __name__ == "__main__":
    app.run(debug=True)