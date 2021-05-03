from app.extensions import db
from datetime import datetime

class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.relationship('LikeModel', backref = 'like_posts', lazy = 'dynamic')
    def __repr__(self):
        return '<Post {}>'.format(self.title)
