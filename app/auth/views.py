from flask import g, redirect, url_for, request, flash, render_template
from flask_login import login_user, logout_user, current_user

from app import login_manager
from app.auth.forms import LoginForm
from app.models import User
from . import auth


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.before_request
def before_request():
    g.user = current_user


@auth.route('/login', methods=['GET', 'POST'])
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

    return render_template('auth/login.html', **{
        'title': 'Sing In',
        'form': form
    })


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))