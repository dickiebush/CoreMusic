from flask_sqlalchemy import SQLAlchemy
from routes import db


class song(db.Model):
    __tablename__ = 'songs'
    url       = db.Column(db.String(150), primary_key = True)
    song_name = db.Column(db.String(150))
    artist    = db.Column(db.String(150))

    def __init__(self, url, song_name, artist):
        self.url = url.lower()
        self.song_name = song_name.lower()
        self.artist = artist.lower()

    def __str__(self):
        return self.url
