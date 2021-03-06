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
from app.main.models.products import ProductModel
from app.main.schemas.product import ProductPaginationSchema, ProductSchema
from app.main.utils import clear_cache

product_schema = ProductSchema()
product_pagiantion_schema = ProductPaginationSchema()


class ProductList(Resource):

    # @requires_access_level(ACCESS['guest'])

    @use_kwargs({
        "page": fields.Int(missing=1),
        'per_page': fields.Int(missing=20),
        'sort': fields.Str(missing='weight'),
        'order': fields.Str(missing='desc')}, location="query")
    @cache.cached(timeout=60, query_string=True)
    @jwt_required
    def get(self, page, per_page, sort, order):
        # json_data = request.get_json()

        # try:
        #     data = product_search_schema.load(json_data)
        # except ValidationError as err:
        #     return err.messages
        products = ProductModel.query.filter(
            ProductModel.name.ilike("%hallo%"))
        products = ProductModel.query.pagination(page, per_page)

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
            clear_cache('/products')
            return schema.dump(new_product), HTTPStatus.CREATED

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR


class Product(Resource):

    # @requires_access_level(ACCESS['user'])
    @cache.cached(timeout=60, query_string=True)
    @jwt_required
    def get(self, id):
        product = ProductModel.find_by_id(id)
        if not product:
            return {'message': 'no product found'}, HTTPStatus.NOT_FOUND

        return product_schema.dump(product), HTTPStatus.OK

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
        if data.get('brand_id') and BrandModel.find_by_id(data.get('brand_id')):
            product.brand_id = data.get('brand_id') or product.brand_id

        product.updatedBy_id = current_user.id

        product.save_to_db()

        clear_cache('/products')

        return product_schema.dump(product), HTTPStatus.OK

    @jwt_required
    def delete(self, id):

        product = ProductModel.find_by_id(id=id)

        if product is None:
            return {'message': 'Product not found'}, HTTPStatus.NOT_FOUND

        product.delete_from_db()

        clear_cache('/products')

        return {}, HTTPStatus.NO_CONTENT
