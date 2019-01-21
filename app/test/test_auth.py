import unittest
import json
from app.main.resources import db
from app.test.base import BaseTestCase


def register_user(self):
    return self.app.post(
        '/registration',
        data=json.dumps(dict(
            username='test',
            password='123456'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.app.post(
        '/auth/login',
        data=json.dumps(dict(
            email='test@test.com',
            password='123456'
        )),
        content_type='application/json'
    )


class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        """ Test for user registration """
        with self.app:
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == 'User test was created')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        register_user(self)
        with self.app:
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)


if __name__ == '__main__':
    unittest.main()
