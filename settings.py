import os
basedir = os.path.abspath(os.path.dirname(__file__))

try:
    from local_settings import *
except ImportError:
    pass

class Config:
    CSRF_ENABLED = True
    SECRET_KEY = '@$#@RRer23$@#$RWEr_)('

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(self):
        pass


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    POSTGRES = {
        'user': 'postgres',
        'pw': '',
        'db': 'microblog_testing',
        'host': 'localhost',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI or 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(
        **POSTGRES)


class DevelopmentConfig(Config):
    DEBUG = True
    POSTGRES = {
        'user': 'postgres',
        'pw': '',
        'db': 'microblog',
        'host': 'localhost',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI or 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(**POSTGRES)


config = {
    'develop': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}

