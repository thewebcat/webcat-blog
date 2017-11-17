from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.moment import Moment
from flask.ext.mail import Mail

from settings import config

db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
toolbar = DebugToolbarExtension()

login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    #app.debug = app.config['DEBUG']
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
