from app.main.extensions import api
from app.main.resources.users.routes import User, UserList

api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/users/<int:id>', endpoint='user')
