from flask import url_for
from marshmallow import fields, INCLUDE, Schema, post_dump, pre_dump
from marshmallow.validate import OneOf
from app.main.models.products import ProductModel
from app.main.schemas.pagination import PaginationSchema
from app.main.models.users import UserModel, ACCESS


def invert_dict(d):
    return dict([(v, k) for k, v in d.items()])


class AccessSchema(fields.Field):

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return invert_dict(ACCESS)[value]

    def _deserialize(self, value, attr, data, **kwargs):
        return value.lower()


class UserSchema(Schema):

    class Meta:
        model = UserModel

    id = fields.Int()
    username = fields.Str(data_key="name")  # change field name with data_key
    access = AccessSchema()


class ProductSearchSchema(Schema):

    page = fields.Int(missing=1)
    per_page = fields.Int(missing=10)
    sort = fields.Str(missing="createdAt")
    order = fields.Str(missing="desc")


class ProductSchema(Schema):

    class Meta:
        ordered = True
        model = ProductModel
        unknown = INCLUDE

    name = fields.Str(required=True)
    weight = fields.Float()
    description = fields.Str()
    # use only to reduce fields to show
    createdBy_id = fields.Int(dump_only=True)
    createdBy = fields.Nested(UserSchema(only=("username",)), dump_only=True)
    updatedBy_id = fields.Int(dump_only=True)
    updatedBy = fields.Nested(UserSchema(), dump_only=True)
    hyperlink = fields.Method("_hyperlink", dump_only=True)

    # use Methode or a function
    # hyperlink = fields.Function(lambda obj: url_for(
    #     'product', id=obj.id, _external=True))

    # @post_dump(pass_many=True)
    # def wrap_with_envelope(self, data, many, **kwargs):
    #     # key = self.opts.plural_name if many else self.opts.name
    #     # if self.opts.createdBy:
    #     #     return{'name2': data['name']}
    #     # else:
    #     #     return {data}

    #     namespace = 'products' if many else 'product'
    #     return {namespace: data}

    def _hyperlink(self, obj):
        # url_for('product', id=obj.id, _external=True)
        return url_for('product', id=obj.id, _external=True)


class ProductPaginationSchema(PaginationSchema):
    data = fields.Nested(ProductSchema, attribute='items', many=True)
