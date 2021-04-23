from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import jsonify
from blacklist import BLACKLIST

bootstrap = Bootstrap()
db = SQLAlchemy()
jwt = JWTManager()
login_manager = LoginManager()
mail = Mail()
moment = Moment()

