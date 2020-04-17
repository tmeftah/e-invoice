from datetime import datetime

import sqlalchemy as sa
from flask_sqlalchemy import Model
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from app.main.resources import db


class BaseMixin(Model):

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


class UserMixin(BaseMixin, Model):

    @declared_attr
    def createdAt(cls):
        return sa.Column(sa.DateTime, default=datetime.utcnow)

    @declared_attr
    def updateAt(cls):
        return sa.Column(sa.DateTime)

    @declared_attr
    def createdBy_id(cls):
        return sa.Column(sa.Integer, ForeignKey('users.id'),
                         nullable=False)

    @declared_attr
    def updatedBy_id(cls):
        return sa.Column(sa.Integer, ForeignKey('users.id'))

    @declared_attr
    def createdBy(cls):
        return relationship(
            'UserModel', foreign_keys=[cls.createdBy_id])

    @declared_attr
    def updatedBy(cls):
        return relationship(
            'UserModel', foreign_keys=[cls.updatedBy_id])
