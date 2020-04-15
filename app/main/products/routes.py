# -*- coding: utf-8 -*-
from datetime import datetime
from http import HTTPStatus
from flask import request, jsonify
from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user
from app.main.resources import api, cache
from app.main.models.products import ProductModel
from app.main.schemas.product import ProductSchema, ProductPaginationSchema, ProductSearchSchema
from app.main.users.decorators import requires_access_level
from app.main.models.users import ACCESS
from app.main.utils import clear_cache, cache_json_keys


product_pagiantion_schema = ProductPaginationSchema()
product_search_schema = ProductSearchSchema()



class ProductList(Resource):

    # @requires_access_level(ACCESS['guest'])

    @cache.cached(timeout=60, key_prefix=cache_json_keys)
    @jwt_required
    def get(self):
        json_data = request.get_json()

        try:
            data = product_search_schema.load(json_data)
        except ValidationError as err:
            return err.messages

        products = ProductModel.get_all_published(
            "", data.get("page"), data.get("per_page"), data.get("sort"), data.get("order"))

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
            return schema.dump(new_product), 201

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR


class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('weight')
    parser.add_argument('name')

   # @jwt_required
   # @requires_access_level(ACCESS['user'])
    @cache.cached(timeout=60, query_string=True)
    def get(self, id):
        product = ProductModel.find_by_id(id)
        if product:
            return product.to_json()
        else:
            return {'message': 'no product found'}, HTTPStatus.NOT_FOUND

    def put(self, id):

        args = self.parser.parse_args()
        product = ProductModel.find_by_id(id)
        if product:
            product.name = args['name']
            product.save_to_db()
            clear_cache('/products')

            return {'message': 'product {} found'.format(args['name'])}, HTTPStatus.OK
        else:
            return {'message': 'no product found'}, HTTPStatus.NOT_FOUND
