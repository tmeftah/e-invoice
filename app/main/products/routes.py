# -*- coding: utf-8 -*-
from datetime import datetime
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from app.main.resources import api
from app.main.models.products import ProductModel
from app.main.users.decorators import requires_access_level
from app.main.models.users import ACCESS


class ProductList(Resource):
    # decorators = [jwt_required]
    # @jwt_required
    # @requires_access_level(ACCESS['guest'])
    id = 0

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No product name provided',
                                   location='json')
        self.reqparse.add_argument('partNumber', type=str, default="000",
                                   location='json')
        self.reqparse.add_argument('weight', type=float, default=0.0,
                                   location='json')
        self.reqparse.add_argument('createdAt', type=datetime, default=datetime.utcnow,
                                   location='json')
        self.reqparse.add_argument('user_id', type=int,
                                   location='json')

        super(ProductList, self).__init__()

    def get(self):
        return ProductModel.return_all()

    def post(self):

        args = self.reqparse.parse_args()

        if ProductModel.find_by_name(args['name']):
            return {'message': "A product with name '{}' already exists. Please choose other refence name.".format(args['name']),
                    'status': 'fail'}, 400

        new_product = ProductModel(
            **args
        )
        try:
            new_product.save_to_db()
            return {'message': 'Product {} was created'.format(args['name']),
                    'status': 'success'}, 201
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
