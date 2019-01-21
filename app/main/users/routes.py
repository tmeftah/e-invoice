from flask_restful import Resource
from flask_jwt_extended import jwt_required
from decorators import requires_access_level
from model import UserModel, ACCESS


class UserList(Resource):
    @jwt_required
    @requires_access_level(ACCESS['guest'])
    def get(self):
        return UserModel.return_all()


class UserPorfile(Resource):
    @jwt_required
    @requires_access_level(ACCESS['guest'])
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        return {
            'username': user.username,
            'access_level': user.access
        }
