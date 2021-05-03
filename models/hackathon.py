from app.extensions import db

class HackathonModel(db.Model):
    __tablename__ = "hackathon"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    description = db.Column(db.String(128))
    url = db.Column(db.String(128))
    date = db.Column(db.DateTime, nullable=False)

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
        return '<Hackathon {}>'.format(self.title)
