# -*- coding: utf-8 -*-
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
            'invoices': [
               {
                   'id': 0,
                   'name': "INV0001",
                   'client': "Client-1",
                   'amount': "159.52",
                   'currency': "$",
                   'term': "2 Days",
                   'due': "01-08-2019"
               },
                {
                   'id': 1,
                   'name': "INV0002",
                   'client': "Client-2",
                   'amount': "200.00",
                   'currency': "€",
                   'term': "Due on Recept",
                   'due': "17-07-2019"
               },
                {
                   'id': 2,
                   'name': "INV0003",
                   'client': "Client-3",
                   'amount': "202.00",
                   'currency': "€",
                   'term': "Due on Recept",
                   'due': "17-07-2019"
               }
            ]
        }


class GetProduct(Resource):
    @jwt_required
    @requires_access_level(ACCESS['user'])
    def get(self):
        return {
            'message': ' index page 2'
        }
