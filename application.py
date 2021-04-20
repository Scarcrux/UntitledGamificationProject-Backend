import os
from flask_migrate import Migrate, upgrade
from app import create_app
from app.extensions import db
from models.user import UserModel, Permission
from models.role import RoleModel

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=UserModel, Role=UserModel,
                Permission=Permission)

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    RoleModel.insert_roles()

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
