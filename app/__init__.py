import logging
from config import config
from logging.handlers import SMTPHandler

from flask import Flask
from .extensions import bootstrap, db, moment, login_manager, mail

from models.achievement import Achievement
from models.comment import Comment
from models.conference import Conference
from models.currency import Currency
from models.hackathon import Hackathon
from models.like import Like
from models.post import Post
from models.project import Project
from models.reward import Reward
from models.role import Role
from models.tag import Tag
from models.user import User

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Blueprint for unauthorized routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Send e-mail logs of production errors
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Gamification Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

    return app

