from app.main.resources import api
from app.main.users.routes import UserList, UserPorfile

api.add_resource(UserList, '/user/list')
api.add_resource(UserPorfile, '/user/<int:user_id>/profile')
