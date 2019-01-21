from ..resources import db
from passlib.hash import pbkdf2_sha256 as sha256


ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}


class UserModel(db.Model):
    """ User Model for storing user details """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
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
    def find_by_id(self, id):
        return self.query.filter_by(id=id).first()

    @classmethod
    def find_by_username(self, username):
        return self.query.filter_by(username=username).first()

    @classmethod
    def return_all(self):
        def to_json(user):
            return {
                'username': user.username,
                'password': user.password
            }
        return {'users': list(map(lambda user: to_json(user), UserModel.query.all()))}

    @classmethod
    def delete_all(self):
        try:
            num_rows_deleted = db.session.query(self).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<User '{}'>".format(self.username)
