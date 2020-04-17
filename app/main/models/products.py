
from sqlalchemy import asc, desc, or_

from app.main.extensions import db
from app.main.models.utils import UserMixin


class ProductModel(UserMixin, db.Model):

    """ Product Model for storing product details """

    __tablename__ = 'products'

    name = db.Column(db.String(120), unique=True, nullable=False)
    partNumber = db.Column(db.String(120))
    status = db.Column(db.Boolean)
    weight = db.Column(db.Float)
    url = db.Column(db.String(120))
    description = db.Column(db.String(120))

    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))

    def __repr__(self):
        return "<Product '{}'>".format(self.name)
