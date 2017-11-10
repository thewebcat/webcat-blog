from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.moment import Moment

app = Flask(__name__)
app.config.from_object('settings')

app.debug = app.config['DEBUG']

db = SQLAlchemy(app)
migrate = Migrate(app, db)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

bootstrap = Bootstrap(app)

moment = Moment(app)

toolbar = DebugToolbarExtension(app)

from app import views, models