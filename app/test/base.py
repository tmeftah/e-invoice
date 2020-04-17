import unittest

from app.main import create_app
from app.main.extensions import db

app = create_app('test')


class BaseTestCase(unittest.TestCase):
    """ Base Tests """

    def setUp(self):

        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
