from email.policy import default
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms import validators
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Events, Place

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Отправить')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

class DateForm(FlaskForm):
    date = SelectField('Выберите дату', choices=[(date.today(), 'Сегодня')], default=date.today())
    def __init__(self, upcoming_events=None):
        super().__init__()  # calls the base initialisation and then...
        if upcoming_events: 
            self.date.choices.extend(list(dict.fromkeys([(events.start_date, events.start_date.strftime('%d.%m.%Y')) for events in upcoming_events])))
    submit = SubmitField('Выбрать')