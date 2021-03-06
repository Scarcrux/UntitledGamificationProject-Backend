import logging
from config import config
from logging.handlers import SMTPHandler
from marshmallow import ValidationError
from flask import Flask, jsonify
from .routes import api
from .extensions import bootstrap, db, jwt, login_manager, ma, mail, moment

from models.achievement import AchievementModel
from models.comment import CommentModel
from models.conference import ConferenceModel
from models.currency import CurrencyModel
from models.hackathon import HackathonModel
from models.like import LikeModel
from models.post import PostModel
from models.project import ProjectModel
from models.reward import RewardModel
from models.role import RoleModel
from models.tag import TagModel
from models.tokenblocklist import TokenBlocklist
from models.user import UserModel


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    api.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    # Callback function to check if a JWT exists in the database blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400

    @app.before_first_request
    def create_tables():
        db.create_all()
    """



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
    """
    return app

