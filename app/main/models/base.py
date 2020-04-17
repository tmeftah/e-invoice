
import sqlalchemy as sa
from flask_sqlalchemy import Model
from sqlalchemy import asc, desc, or_


class BaseModel(Model):

    id = sa.Column(sa.Integer, primary_key=True)

    @classmethod
    def get_all_published(cls, q, page, per_page, sort, order, **kwargs):

        keyword = '%{keyword}%'.format(keyword=q)

        if order == 'asc':
            sort_logic = asc(getattr(cls, sort))
        else:
            sort_logic = desc(getattr(cls, sort))

        if hasattr(cls, 'username'):
            name = cls.username
        else:
            name = cls.name

        return cls.query.filter(name.ilike(keyword)).order_by(sort_logic).paginate(page=page, per_page=per_page)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
