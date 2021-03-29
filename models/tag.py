from app import db

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))

    def __repr__(self):
        return '<Tag {}>'.format(self.title)
