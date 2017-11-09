from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('settings')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

bootstrap = Bootstrap(app)

from app import views, models