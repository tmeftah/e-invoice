from passlib.hash import pbkdf2_sha256 as sha256

from app.main.extensions import db
from app.main.models.utils import BaseMixin

ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}


class UserModel(BaseMixin, db.Model):
    """ User Model for storing user details """
    __tablename__ = 'users'

    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    access = db.Column(db.Integer)

    def is_admin(self):
        return self.access == ACCESS['admin']

    def allowed(self, access_level):
        return self.access >= access_level

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)
