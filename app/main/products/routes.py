from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ..resources import api
from ..users.decorators import requires_access_level
from ..users.model import ACCESS


class List(Resource):
    @jwt_required
    @requires_access_level(ACCESS['guest'])
    def get(self):
        return {
            'message': ' index page'
        }


class GetProduct(Resource):
    @jwt_required
    @requires_access_level(ACCESS['user'])
    def get(self):
        return {
            'message': ' index page 2'
        }
