import unittest

from app.main import db
from manage import app


class BaseTestCase(unittest.TestCase):
    """ Base Tests """

    def setUp(self):
        app.config.from_object('app.main.config.TestingConfig')
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
