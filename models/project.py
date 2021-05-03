from app.extensions import db
from datetime import datetime
from .follower import follower
from .tag import TagModel
from .tag_project import tag_project
from typing import List
class ProjectModel(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('TagModel', secondary=tag_project,
        backref=db.backref('projects', lazy='dynamic'),lazy = 'dynamic')
    favorites = db.relationship('FavoriteModel', backref = 'favorite_projects', lazy = 'dynamic')

    def tags_projects(self):
        return TagModel.query.join(tag_project).join(ProjectModel).filter(tag_project.c.project_id == self.id).order_by(TagModel.title)

    #@classmethod
    #def find_by_username(cls, username):
    #    return cls.query.filter_by(username=username).first()

    #@classmethod
    #def find_by_title(cls, email: str) -> "ProjectModel":
    #    return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_name(cls, name: str) -> "ProjectModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["ProjectModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

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
