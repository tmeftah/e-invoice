# -*- coding: utf-8 -*-
from datetime import datetime
from http import HTTPStatus
from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user
from webargs import fields
from webargs.flaskparser import use_kwargs
from app.main.resources import api, cache
from app.main.models.products import ProductModel
from app.main.schemas.product import ProductSchema, ProductPaginationSchema, ProductSearchSchema
from app.main.users.decorators import requires_access_level
from app.main.models.users import ACCESS
from app.main.utils import clear_cache, cache_json_keys

product_schema = ProductSchema()
product_pagiantion_schema = ProductPaginationSchema()


class ProductList(Resource):

    # @requires_access_level(ACCESS['guest'])

    # @cache.cached(timeout=60, key_prefix=cache_json_keys)
    @jwt_required
    @use_kwargs({'q': fields.Str(missing=''),
                 'page': fields.Int(missing=1),
                 'per_page': fields.Int(missing=20),
                 'sort': fields.Str(missing='weight'),
                 'order': fields.Str(missing='desc')})
    def get(self, q, page, per_page, sort, order):

        # json_data = request.get_json()

        # try:
        #     data = product_search_schema.load(json_data)
        # except ValidationError as err:
        #     return err.messages
        products = ProductModel.get_all_published(
            "",  page, per_page, sort, order)

        return product_pagiantion_schema.dump(products)

    @jwt_required
    def post(self):
        json_data = request.get_json()
        schema = ProductSchema(exclude=("hyperlink",))
        try:
            data = schema.load(json_data)
        except ValidationError as err:
            return err.messages

        if ProductModel.find_by_name(data.get("name")):
            return {'message': "A product with name '{}' already exists. Please choose other refence name.".format(data.get("name")),
                    'status': 'fail'}, HTTPStatus.BAD_REQUEST

        try:
            new_product = ProductModel(**data)
            new_product.createdBy_id = current_user.id
            new_product.save_to_db()
            return schema.dump(new_product), HTTPStatus.CREATED

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR


class Product(Resource):

   # @jwt_required
   # @requires_access_level(ACCESS['user'])
    @cache.cached(timeout=60, query_string=True)
    def get(self, id):
        product = ProductModel.find_by_id(id)
        if product:
            return product.to_json()
        else:
            return {'message': 'no product found'}, HTTPStatus.NOT_FOUND

    @jwt_required
    def put(self, id):

        json_data = request.get_json()
        try:
            data = product_schema.load(data=json_data, partial=('name',))
        except ValidationError as err:
            return err.messages

        product = ProductModel.find_by_id(id)

        if product is None:
            return {'message': 'Product not found'}, HTTPStatus.NOT_FOUND

        product.name = data.get('name') or product.name
        product.description = data.get('description') or product.description
        product.partNumber = data.get('partNumber') or product.partNumber

        product.updatedBy_id = current_user.id

        product.save_to_db()

        clear_cache('/products')

        return product_schema.dump(product), HTTPStatus.OK
