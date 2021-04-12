from datetime import datetime
import hashlib

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin

from app import db, login_manager
from .follower import follower
from .post import Post
from .role import Role

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique=True)
    email = db.Column(db.String(128), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    member_since = db.Column(db.DateTime, default = datetime.utcnow)
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)
    about_me = db.Column(db.Text())
    post = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
      'User', secondary = follower,
      primaryjoin = (follower.c.follower_id == id),
      secondaryjoin = (follower.c.followed_id == id),
      backref = db.backref('follower', lazy = 'dynamic'), lazy = 'dynamic')
    avatar_hash = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['GAMIFICATION_ADMIN']:
                self.role = Role.query.filter_by(name = 'Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default = True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
               data = s.loads(token.encode('utf-8'))
        except:
              return False
        user = User.query.get(data.get('reset'))
        if user is None:
              return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
               {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
               data = s.loads(token.encode('utf-8'))
        except:
              return False
        if data.get('change_email') != self.id:
              return False
        new_email = data.get('new_email')
        if new_email is None:
              return False
        if self.query.filter_by(email=new_email).first() is not None:
               return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def followed_posts(self):
        followed = Post.query.join(
            follower, (follower.c.followed_id == Post.user_id)).filter(
                follower.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            follower.c.followed_id == user.id).count() > 0

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
      	return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
       return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
