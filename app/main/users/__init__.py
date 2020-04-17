from app.main.resources import api
from app.main.users.routes import User, UserList

api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/users/<int:id>', endpoint='user')
