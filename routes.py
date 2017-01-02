from flask import Flask, render_template
from models import db, Song
import os
import core

# magical incantations 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    # is while within this block. Therefore, you can now run........

db.init_app(app)

with app.app_context():
    db.create_all()
    db.session.commit()

#from models import Song
@app.route("/")
def index():

    return ("Bout to run some shit nigga")

@app.route("/run")
def run():
    core.run_script(db)
    return("process done")



if __name__ == "__main__":
    app.run(debug=True)