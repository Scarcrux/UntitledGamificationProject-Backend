import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True  # enable blacklist feature
    JWT_BLACKLIST_TOKEN_CHECKS = [
        "access",
        "refresh",
    ]  # allow blacklisting for access and refresh tokens
    STREAM_SECRET = os.environ.get('STREAM_SECRET')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
      ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GAMIFICATION_MAIL_SUBJECT_PREFIX = '[Gamification]'
    GAMIFICATION_MAIL_SENDER = 'Gamification Admin <admin@gamification.co>'
    GAMIFICATION_ADMIN = os.environ.get('GAMIFICATION_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
      pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
      'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
