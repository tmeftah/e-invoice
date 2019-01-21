from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, reqparse
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
api = Api()
jwt = JWTManager()
