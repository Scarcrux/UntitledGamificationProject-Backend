from app.extensions import db
from datetime import datetime

class LikeModel(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Like {}>'.format(self.user_id)
