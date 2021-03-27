from app import db
class Currency(db.Model):
    __tablename__ = "currency"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    owner = db.relationship("Owner", uselist=False, back_populates="currency")

    def __repr__(self):
        return '<Currency {}>'.format(self.title)
