from flask import url_for
from marshmallow import INCLUDE, Schema, fields
from marshmallow.validate import Length

from app.main.models.products import ProductModel
from app.main.schemas.brands import BrandSchema
from app.main.schemas.pagination import PaginationSchema
from app.main.schemas.users import UserSchema


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
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=120))
    weight = fields.Float()
    description = fields.Str(validate=Length(max=120))
    brand_id = fields.Int()
    brand = fields.Nested(BrandSchema(only=('name',)), dump_only=True)
    partNumber = fields.Str(validate=Length(max=120))
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
    products = fields.Nested(ProductSchema, attribute='items', many=True)
