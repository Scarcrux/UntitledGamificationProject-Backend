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

# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    #print(other)
    #print (decrypted_token["jti"])
    return jwt_payload["jti"] in BLACKLIST
