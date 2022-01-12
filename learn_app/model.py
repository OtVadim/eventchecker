from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from learn_app import db, login
from flask_login import LoginManager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(70), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    user_comments = db.relationship ('Comments', backref = 'user', lazy = True)

    def __repr__(self):
        return "<User {}>".format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

