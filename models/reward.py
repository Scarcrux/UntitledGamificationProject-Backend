from app import db
from datetime import datetime

class Reward(db.Model):
    __tablename__ = 'reward'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer)
    description = db.Column(db.String(128))
    cost = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Reward {}>'.format(self.title)
