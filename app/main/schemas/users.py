from flask import url_for
from marshmallow import Schema, fields
from marshmallow.validate import Length

from app.main.models.users import ACCESS, UserModel
from app.main.schemas.pagination import PaginationSchema


def invert_dict(d):
    return dict([(v, k) for k, v in d.items()])


class AccessSchema(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ACCESS["guest"]
        return invert_dict(ACCESS)[value]

    def _deserialize(self, value, attr, data, **kwargs):
        return value.lower()


class UserSchema(Schema):

    class Meta:
        ordered = True
        model = UserModel

    id = fields.Int(dump_only=True)
    # change field name with data_key
    password = fields.Str(validate=Length(max=120), load_only=True)
    username = fields.Str(validate=Length(max=120),
                          data_key="username", dump_only=True)
    access = AccessSchema()
    hyperlink = fields.Method("_hyperlink", dump_only=True)

    def _hyperlink(self, obj):
        # url_for('product', id=obj.id, _external=True)
        return url_for('users', id=obj.id, _external=True)


class UserPaginationSchema(PaginationSchema):
    users = fields.Nested(UserSchema, attribute='items', many=True)
