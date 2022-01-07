from flask_sqlalchemy import SQLAlchemy
from learn_app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(70), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    user_comments = db.relationship ('Comments', backref = 'user', lazy = True)

    def __repr__(self):
        return "<User {}>".format(self.email)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey ('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey ('events.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.String, nullable=False)
    

    def __repr__(self):
        return "<Comments {}>".format(self.text)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    publication_date = db.Column(db.DateTime, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey ('place.id'), nullable=False)
    slug = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String, nullable=False) #город проведения
    categories = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=True)
    age_restriction = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=True)
    is_free = db.Column(db.Boolean, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    is_continuous = db.Column(db.Boolean, nullable=True)
    event_comments = db.relationship('Comments', backref = 'event', lazy=True)
    event_image = db.relationship('EventImage', backref = 'image', lazy=True)

    def __repr__(self):
        return "<Events {}>".format(self.title)

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    event_place = db.relationship('Events', backref='place', lazy=True)
    

    def __repr__(self):
        return "<Place {}>".format(self.title)


class EventImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey ('events.id'), nullable=False)
    url = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<EventImage {}>".format(self.url)

