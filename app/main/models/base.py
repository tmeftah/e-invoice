
import sqlalchemy as sa
from flask_sqlalchemy import BaseQuery, Model
from sqlalchemy import asc, desc, or_


class BaseQueryCollection(BaseQuery):

    def pagination(self, page, per_page):
        return self.paginate(page=page, per_page=per_page)


class BaseModel(Model):

    id = sa.Column(sa.Integer, primary_key=True)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
