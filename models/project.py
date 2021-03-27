from app import db
from datetime import datetime
from .follower import follower
from .tag_project import tag_project
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tagged = db.relationship("Tag",
        secondary=tag_project,
        backref="tag")

    def tag(self, tag):
        if not self.is_tagging(tag):
            self.tagged.append(tag)

    def untag(self, tag):
        if self.is_tagging(tag):
            self.tagged.remove(tag)

    def is_tagging(self, tag):
        return self.tagged.filter(
            tag_project.c.project_id == tag.id).count() > 0

    def __repr__(self):
        return '<Project {}>'.format(self.title)
