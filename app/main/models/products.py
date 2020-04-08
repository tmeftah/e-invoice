from datetime import datetime
from app.main.resources import db


class ProductModel(db.Model):
    """ User Model for storing user details """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    partNumber = db.Column(db.String(120))
    status = db.Column(db.Boolean)
    weight = db.Column(db.Float)
    url = db.Column(db.String(120))
    description = db.Column(db.String(120))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updateAt = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    user = db.relationship('UserModel')

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def return_all(cls):
        return {'products': list(map(lambda product: cls.to_json(product), ProductModel.query.all()))}

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'weight': self.weight,
            'url': self.url,
            'description': self.description,
            'createAt': str(self.createdAt),
            'updateAt': str(self.updateAt)
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Product '{}'>".format(self.name)
