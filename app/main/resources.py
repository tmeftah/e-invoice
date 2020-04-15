from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, reqparse
from flask_jwt_extended import JWTManager
from flask_caching import Cache


db = SQLAlchemy()
api = Api()
jwt = JWTManager()
cache = Cache()
