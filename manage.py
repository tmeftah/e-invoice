import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from flask import current_app

from app.main import db
from app.main import create_app
from app.main.users.model import UserModel


app = create_app('dev')
manager = Manager(app)
migrate = Migrate(app, db)


@manager.command
def run():
    app.run(debug=True)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=UserModel)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
