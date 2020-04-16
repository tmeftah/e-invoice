from datetime import datetime
from flask_sqlalchemy import Model
from sqlalchemy.exc import DatabaseError
from sqlalchemy import asc, desc, or_
from sqlalchemy.ext.declarative import declared_attr
from app.main.resources import db
from app.main.models.base import UserMixin


class BrandModel(UserMixin, db.Model):

    """ Brand Model for sorting Brand details """

    __tablename__ = 'brands'

    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120))
    website = db.Column(db.String(120))


class ProductModel(UserMixin, db.Model):

    """ Product Model for storing product details """

    __tablename__ = 'products'

    name = db.Column(db.String(120), unique=True, nullable=False)
    partNumber = db.Column(db.String(120))
    status = db.Column(db.Boolean)
    weight = db.Column(db.Float)
    url = db.Column(db.String(120))
    description = db.Column(db.String(120))

    @classmethod
    def get_all_published(cls, q, page, per_page, sort, order):

        keyword = '%{keyword}%'.format(keyword=q)

        if order == 'asc':
            sort_logic = asc(getattr(cls, sort))
        else:
            sort_logic = desc(getattr(cls, sort))

        return cls.query.filter(or_(cls.name.ilike(keyword),
                                    cls.description.ilike(keyword))). \
            order_by(sort_logic).paginate(page=page, per_page=per_page)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def return_all(cls):
        return {'products': list(map(cls.to_json, ProductModel.query.all()))}

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

        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def __repr__(self):
        return "<Product '{}'>".format(self.name)
