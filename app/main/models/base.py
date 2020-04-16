from datetime import datetime

import sqlalchemy as sa
from flask_sqlalchemy import Model
from sqlalchemy.ext.declarative import declared_attr


class BaseModel(Model):

    id = sa.Column(sa.Integer, primary_key=True)


class UserMixin(Model):

    @declared_attr
    def createdAt(cls):
        return sa.Column(sa.DateTime, default=datetime.utcnow)

    @declared_attr
    def updateAt(cls):
        return sa.Column(sa.DateTime)

    @declared_attr
    def createdBy_id(cls):
        return sa.Column(sa.Integer, sa.ForeignKey('users.id'),
                         nullable=False)

    @declared_attr
    def updatedBy_id(cls):
        return sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    @declared_attr
    def createdBy(cls):
        return sa.orm.relationship(
            'UserModel', foreign_keys=[cls.createdBy_id])

    @declared_attr
    def updatedBy(cls):
        return sa.orm.relationship(
            'UserModel', foreign_keys=[cls.updatedBy_id])
