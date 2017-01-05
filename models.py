from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Song(db.Model):
    __tablename__ = 'songs'
    url      = db.Column(db.String(150), primary_key = True)
    song_name = db.Column(db.String(150))
    artist   = db.Column(db.String(150))

    def __init__(self, url, song_name, artist):
        self.url = url.lower()
        self.song_name = song_name.lower()
        self.artist = artist.lower()

    def __str__(self):
        return self.url

class User(db.Model):
    __tablename__ = 'users'
    email  = db.Column(db.String(150), primary_key = True)
    name   = db.Column(db.String(150))
    number = db.Column(db.String(15), unique = True)
    artists = db.Column(db.String(250))
    password = db.Column(db.String(20))

    def __init__(self, email, name, number, artists, password):
        self.email    = email
        self.name     = name
        self.number   = number
        self.artists  = artists
        self.password = password

    def __str__(self):
        return self.email