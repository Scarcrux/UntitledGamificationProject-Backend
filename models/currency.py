from app.extensions import db
from sqlalchemy import Column, Integer, ForeignKey
class CurrencyModel(db.Model):
    __tablename__ = "currency"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = db.relationship("UserModel", backref="currency")

    def __repr__(self):
        return '<Currency {}>'.format(self.title)
