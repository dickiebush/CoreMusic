from flask import Flask, render_template, request, redirect, url_for
from models import db, Song, User
import os
from forms import SignupForm
import requests
#import core

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
            with app.app_context():
                db.session.add(user)
                db.session.commit()
            return "Welcome to Core Music!"
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)