from flask import Flask, render_template, request, redirect, url_for
from models import db, Song, User
import os
from forms import SignupForm
import requests

# link to database used for heroku 
# DATABASE_URL=$(heroku config:get DATABASE_URL -a coremusic)

# magical incantations 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    # is while within this block. Therefore, you can now run........
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


if __name__ == "__main__":
    app.run(debug=True)