from app import db

class Hackathon(db.Model):
    __tablename__ = "hackathon"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    description = db.Column(db.String(128))
    url = db.Column(db.String(128))
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Hackathon {}>'.format(self.title)
