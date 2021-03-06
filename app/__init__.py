from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
login = LoginManager(app)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

from app import models, routes