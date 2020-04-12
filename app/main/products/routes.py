# -*- coding: utf-8 -*-
from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user
from app.main.resources import api
from app.main.models.products import ProductModel
from app.main.schemas.product import ProductSchema, ProductPaginationSchema, ProductSearchSchema
from app.main.users.decorators import requires_access_level
from app.main.models.users import ACCESS


product_pagiantion_schema = ProductPaginationSchema()
product_search_schema = ProductSearchSchema()


class ProductList(Resource):

    @jwt_required
    # @requires_access_level(ACCESS['guest'])
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
                    'status': 'fail'}, 400

        try:
            new_product = ProductModel(**data)
            new_product.createdBy_id = current_user.id
            new_product.save_to_db()
            return schema.dump(new_product), 201

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class Product(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('weight')
    parser.add_argument('name')

   # @jwt_required
   # @requires_access_level(ACCESS['user'])
    def get(self, id):
        product = ProductModel.find_by_id(id)
        if product:
            return product.to_json()
        else:
            return {'msg': 'no product found'}, 404

    def put(self, id):

        args = self.parser.parse_args()
        product = ProductModel.find_by_id(id)
        if product:
            product.name = args['name']
            product.save_to_db()

            return {'msg': 'product {} found'.format(args['name'])}, 200
        else:
            return {'msg': 'no product found'}, 404
