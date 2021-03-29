from datetime import datetime, timedelta
import unittest
from app import create_app, db
from models.project import Project
from models.tag import Tag

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app = create_app('testing')
        ctx = app.app_context()
        ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_tag(self):
        u1 = Project(title='john', body='john@example.com')
        u2 = Tag(title='flask')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.tags.all(), [])
        self.assertEqual(u2.projects.all(), [])

        u1.tag(u2)
        db.session.commit()
        self.assertTrue(u1.is_tagging(u2))
        self.assertEqual(u1.tags.count(), 1)
        self.assertEqual(u1.tags.first().title, 'flask')
        self.assertEqual(u2.projects.count(), 1)
        self.assertEqual(u2.projects.first().title, 'john')

        u1.untag(u2)
        db.session.commit()
        self.assertFalse(u1.is_tagging(u2))
        self.assertEqual(u1.tags.count(), 0)
        self.assertEqual(u2.projects.count(), 0)

    def test_tag_posts(self):
        # create four projects
        u1 = Project(title='john', body='john@example.com')
        u2 = Project(title='susan', body='susan@example.com')
        u3 = Project(title='mary', body='mary@example.com')
        u4 = Project(title='david', body='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four tags
        p1 = Tag(title="a")
        p2 = Tag(title="b")
        p3 = Tag(title="c")
        p4 = Tag(title="d")
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # set up the tags
        u1.tag(p2)
        u1.tag(p4)
        u2.tag(p3)
        u3.tag(p4)
        db.session.commit()

        # check the tags of each project
        f1 = u1.tags_projects().all()
        f2 = u2.tags_projects().all()
        f3 = u3.tags_projects().all()
        f4 = u4.tags_projects().all()
        self.assertEqual(f1, [p2, p4])
        self.assertEqual(f2, [p3])
        self.assertEqual(f3, [p4])
        self.assertEqual(f4, [])

if __name__ == '__main__':
    unittest.main(verbosity=2)
