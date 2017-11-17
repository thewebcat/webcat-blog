from flask.ext.wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email


class LoginForm(FlaskForm):
    email = StringField('Enter your email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm(FlaskForm):
    nickname = StringField('Enter your nickname', validators=[DataRequired()])
    email = StringField('Enter your email', validators=[DataRequired()])
    password = PasswordField('Set new Password', [
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')