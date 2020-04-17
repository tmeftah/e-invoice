from flask import url_for
from marshmallow import Schema, fields
from marshmallow.validate import Length

from app.main.models.brands import BrandModel
from app.main.schemas.pagination import PaginationSchema


class BrandSchema(Schema):

    class Meta:

        ordered = True
        model = BrandModel

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=Length(max=120))
    description = fields.Str(validate=Length(max=120))
    website = fields.URL(require_tld=False, validate=Length(max=120))
    hyperlink = fields.Method("_hyperlink", dump_only=True)

    def _hyperlink(self, obj):
        # url_for('product', id=obj.id, _external=True)
        return url_for('brand', id=obj.id, _external=True)


class BrandPaginationSchema(PaginationSchema):
    brands = fields.Nested(BrandSchema, attribute='items', many=True)
