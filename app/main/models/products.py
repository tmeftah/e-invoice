from datetime import datetime
from sqlalchemy.exc import DatabaseError
from sqlalchemy import asc, desc, or_
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
    createdBy_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                             nullable=False)
    updatedBy_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    createdBy = db.relationship(
        'UserModel', backref="createdBy", foreign_keys=[createdBy_id])
    updatedBy = db.relationship(
        'UserModel', backref="updatedBy", foreign_keys=[updatedBy_id])

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
