from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from learn_app import db

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(70), index = True, unique = True)

    def __repr__(self):
        return "<User {}>".format(self.email)