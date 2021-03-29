from app import db
from datetime import datetime
from .follower import follower
from .tag import Tag
from .tag_project import tag_project
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=tag_project,
        backref=db.backref('projects', lazy='dynamic'),lazy = 'dynamic')

    def tags_projects(self):
        return Tag.query.join(tag_project).join(Project).filter(tag_project.c.project_id == self.id).order_by(Tag.title)

    def tag(self, tag):
        if not self.is_tagging(tag):
            self.tags.append(tag)

    def untag(self, tag):
        if self.is_tagging(tag):
            self.tags.remove(tag)

    def is_tagging(self, tag):
        return self.tags.filter(
            tag_project.c.tag_id == tag.id).count() > 0

    def __repr__(self):
        return '<Project {}>'.format(self.title)
