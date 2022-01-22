from asyncio import events
from datetime import date, timedelta
from flask import Flask, render_template, redirect, url_for, flash, request
from sqlalchemy import func
from flask_login.utils import login_required
from app import app, login
from wtforms.validators import DataRequired, Email
from flask_login import current_user, login_user, logout_user
from app.models import User, Events, Place, Comments, EventImage
from app import db
from app.forms import RegistrationForm, LoginForm, DateForm
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    main_title = 'Главная'
    events_today = Events.query.filter_by(start_date = date.today()).all()
    form = DateForm()
    upcoming_events = Events.query.filter(Events.start_date >= date.today()).filter(Events.start_date < date.today() + timedelta(days=30)).all()
    form.date.choices.extend([(events.start_date, events.start_date) for events in upcoming_events])
    if form.validate_on_submit():
        events_today = Events.query.filter_by(start_date = form.date.data).all()
        return render_template('index.html', main_title=main_title, events_today=events_today, form=form)
    return render_template('index.html', main_title=main_title, events_today=events_today, form=form)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    reg_title = 'Регистрация'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        user = User(username=reg_form.username.data, email=reg_form.email.data)
        user.set_password(reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!')
        return redirect(url_for('login'))
    else:
        flash('Что пошло не так...')
    return render_template('register.html', page_title = reg_title, form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Авторизация"
    login_form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.email.data)
        next_page = request.args.get('index')
        flash('Вы успешно авторизованы!')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('registration')
        return redirect(next_page)
    return render_template('login.html', page_title=title, log_form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
