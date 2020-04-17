

from app.main.extensions import db
from app.main.models.utils import UserMixin


class BrandModel(UserMixin, db.Model):

    """ Brand Model for sorting Brand details """

    __tablename__ = 'brands'

    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120))
    website = db.Column(db.String(120))
    products = db.relationship('ProductModel', backref='brand')

    def __repr__(self):
        return "<Brand '{}'>".format(self.name)
