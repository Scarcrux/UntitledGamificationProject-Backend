from app.extensions import db
from sqlalchemy import Column, Integer, ForeignKey
class CurrencyModel(db.Model):
    __tablename__ = "currency"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = db.relationship("UserModel", backref="currency")

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Currency {}>'.format(self.title)
