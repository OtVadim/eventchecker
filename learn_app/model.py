from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from learn_app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(70), index = True, unique = True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.email)