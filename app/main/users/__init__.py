from ..resources import api
from . routes import UserList, UserPorfile

api.add_resource(UserList, '/user/list')
api.add_resource(UserPorfile, '/user/<int:user_id>/profile')
