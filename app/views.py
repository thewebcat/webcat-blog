# -*- coding: utf-8 -*-
from datetime import datetime

from app import app, db, models, lm
from flask import render_template, flash, redirect, url_for, g, session, request
from flask_login import current_user, login_required, login_user, logout_user

from app.forms import LoginForm, RegisterForm
from app.models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [  # список выдуманных постов
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        }, {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', **{
        'title': '',
        'user': user,
        'posts': posts,
        'current_time': datetime.utcnow(),
    })


@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            form.nickname.data,
            form.password.data,
            form.email.data,
        )
        db.session.add(user)
        db.session.commit()
        flash('User {} successfully added'.format(user))
        return redirect(url_for('index'))

    return render_template('register.html', **{
        'title': 'Registration in app',
        'form': form,
    })


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        registered_user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if registered_user is None:
            flash('Username or Password is invalid', 'error')
            return redirect(url_for('login'))
        remember_me = False
        if form.remember_me.data:
            remember_me = True
        login_user(registered_user, remember=remember_me)
        flash('Logged in successfully')
        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', **{
        'title': 'Sing In',
        'form': form,
        'providers': app.config['OPENID_PROVIDERS']
    })


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User {} not found.'.format(nickname))
        return redirect(url_for('index'))
    posts = [
        { 'author': user, 'body': 'Test post #1' },
        { 'author': user, 'body': 'Test post #2' }
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
