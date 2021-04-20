from app.extensions import db

tag_project = db.Table('tag_project',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)
