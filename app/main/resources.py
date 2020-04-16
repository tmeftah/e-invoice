from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.main.models.base import BaseModel

db = SQLAlchemy(model_class=BaseModel)
api = Api()
jwt = JWTManager()
cache = Cache()
