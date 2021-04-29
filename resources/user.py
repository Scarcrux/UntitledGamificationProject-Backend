from flask_restful import Resource
from flask import request, render_template, make_response
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from models.user import UserModel
from models.tokenblocklist import TokenBlocklist
from datetime import datetime
from datetime import timezone
from app.extensions import db
from schemas.user import UserSchema
from marshmallow import ValidationError
from app.email import send_email

BLANK_ERROR = "'{}' cannot be blank."
USER_ALREADY_EXISTS = "A user with that username already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={}> successfully logged out."
NOT_CONFIRMED_ERROR = "You have not confirmed registration, please check e-mail."
USER_CONFIRMED = "User confirmed."

user_schema = UserSchema()

class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return {"message": USER_ALREADY_EXISTS}, 400

        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)

        user = UserModel.find_by_username(user_data.username)

        if user and safe_str_cmp(user_data.password, user.password):
            if user.confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            return {"message": NOT_CONFIRMED_ERROR.format(user.username)}, 400

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        user_id = get_jwt_identity()
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200
    #def post(cls):
    #    jti = get_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
    #    user_id = get_jwt_identity()
    #    BLACKLIST.add(jti)
    #


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200

class ConfirmToken(Resource):
    @classmethod
    @jwt_required()
    def get(cls, token):
        print (token)
        user_id = get_jwt_identity()
        print(user_id)
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        #if user.confirmed:
            headers = {"Content-Type": "text/html"}
            return make_response(
            render_template("confirmation_page.html", email=user.username), 200, headers)

        if user.confirm(token):
            user.confirmed = True
            user.save_to_db()
            headers = {"Content-Type": "text/html"}
            return make_response(
            render_template("confirmation_page.html", email=user.username), 200, headers)

        #else:
        return {"message": 'The confirmation link is invalid or has expired.'}, 401
        #return {"message": USER_CONFIRMED}, 200
        # return redirect("http://localhost:3000/", code=302)  # redirect if we have a separate web app

class Confirm(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        user_id = get_jwt_identity()
        print(user_id)
        current_user = UserModel.find_by_id(user_id)
        print(current_user)
        if not current_user:
            return {"message": USER_NOT_FOUND}, 404
        token = current_user.generate_confirmation_token()
        send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm_user', user=current_user, token=token)
        return {"message": 'A new confirmation email has been sent to you by email.'}, 200

class Reset(Resource):
    @classmethod
    def get(cls):
        user_json = request.get_json()
        user = UserModel.query.filter_by(email = user_json['email']).first()
        print(user)
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token)
            return {"message": 'A reset password email has been sent to you.'}, 200
        return {"message": 'Cannot find email address.'}, 404

class ResetPassword(Resource):
    @classmethod
    def post(cls, token):
        user_json = request.get_json()
        if UserModel.reset_password(token, user_json['password']):
            db.session.commit()
            return {"message": 'Your password has been updated.'}, 200
        return {"message": 'Token is invalid or expired.'}, 404

"""


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)
"""
