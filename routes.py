from flask import Flask, render_template

import core

# magical incantations 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/songs'
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    # is while within this block. Therefore, you can now run........
db = SQLAlchemy(app)

from models import Song

@app.route("/")
def index():

    core.run_script(db)
    return ("Bout to run some shit nigga")

if __name__ == "__main__":
    app.run(debug=True)