# -*- coding: utf-8 -*-
from datetime import datetime

from flask import render_template, flash, redirect, url_for, g, request, abort
from flask_login import current_user, login_required, login_user, logout_user

from app import db, login_manager
from . import main
from .forms import LoginForm, RegisterForm
from ..models import User





@main.route('/')
@main.route('/index')
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


@main.route('/registration', methods=['GET', 'POST'])
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





@main.route('/user/<nickname>')
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

