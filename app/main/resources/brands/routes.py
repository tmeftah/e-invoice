# -*- coding: utf-8 -*-

from http import HTTPStatus

from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from webargs import fields
from webargs.flaskparser import use_kwargs

from app.main.extensions import cache
from app.main.models.brands import BrandModel
from app.main.schemas.brands import BrandPaginationSchema, BrandSchema
from app.main.utils import clear_cache

brand_schema = BrandSchema()
brand_pagiantion_schema = BrandPaginationSchema()


class BrandList(Resource):

    # @requires_access_level(ACCESS['guest'])

    # @cache.cached(timeout=60, key_prefix=cache_json_keys)
    @use_kwargs({
        "page": fields.Int(missing=1),
        'per_page': fields.Int(missing=20),
        'sort': fields.Str(missing='id'),
        'order': fields.Str(missing='asc')}, location="query")  # set location to query for pagination
    @cache.cached(timeout=60, query_string=True)
    @jwt_required
    def get(self, page, per_page, sort, order):

        # json_data = request.get_json()
        # except ValidationError as err:
        #     return err.messages

        products = BrandModel.query.pagination(page, per_page)

        return brand_pagiantion_schema.dump(products)

    @jwt_required
    def post(self):
        json_data = request.get_json()
        schema = BrandSchema(exclude=("hyperlink",))
        try:
            data = schema.load(json_data)
        except ValidationError as err:
            return err.messages

        if BrandModel.find_by_name(data.get("name")):
            return {'message': "A brand with name '{}' already exists. Please choose other refence name.".format(data.get("name")),
                    'status': 'fail'}, HTTPStatus.BAD_REQUEST

        try:
            new_brand = BrandModel(**data)
            new_brand.createdBy_id = current_user.id
            new_brand.save_to_db()
            clear_cache('/brands')
            return schema.dump(new_brand), HTTPStatus.CREATED

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR


class Brand(Resource):

   # @jwt_required
   # @requires_access_level(ACCESS['user'])
    @cache.cached(timeout=60, query_string=True)
    @jwt_required
    def get(self, id):

        brand = BrandModel.find_by_id(id)
        if not brand:
            return {'message': 'no brand found'}, HTTPStatus.NOT_FOUND

        return brand_schema.dump(brand), HTTPStatus.OK

    @jwt_required
    def put(self, id):

        json_data = request.get_json()
        try:
            data = brand_schema.load(data=json_data, partial=('name',))
        except ValidationError as err:
            return err.messages

        brand = BrandModel.find_by_id(id)

        if brand is None:
            return {'message': 'Brand not found'}, HTTPStatus.NOT_FOUND

        brand.name = data.get('name') or brand.name
        brand.website = data.get('website') or brand.website

        brand.updatedBy_id = current_user.id

        brand.save_to_db()

        clear_cache('/brands')

        return brand_schema.dump(brand), HTTPStatus.OK

    @jwt_required
    def delete(self, id):

        brand = BrandModel.find_by_id(id=id)

        if brand is None:
            return {'message': 'Brand not found'}, HTTPStatus.NOT_FOUND

        brand.delete_from_db()

        clear_cache('/brands')

        return {}, HTTPStatus.NO_CONTENT
