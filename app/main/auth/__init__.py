from app.main.auth.routes import (GetTokenList, ModifyToken, TokenRefresh,
                                  UserLogin, UserLogoutAccess,
                                  UserLogoutRefresh, UserRegistration)
from app.main.resources import api

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(GetTokenList, '/user/token/list')
api.add_resource(TokenRefresh, '/user/token/refresh')
api.add_resource(ModifyToken, '/user/token/<int:token_id>/modif')
api.add_resource(UserLogoutAccess, '/logout')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
