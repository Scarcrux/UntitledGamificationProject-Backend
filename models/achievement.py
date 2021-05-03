from app.extensions import db

class AchievementModel(db.Model):
    __tablename__ = "achievement"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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
        return '<Achievement {}>'.format(self.title)
