from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.main.models.users import ACCESS, UserModel
from app.main.users.decorators import requires_access_level


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
