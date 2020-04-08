from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.main.models.users import UserModel


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user:
                user = UserModel.find_by_username(current_user)
                if not user:
                    return {'message': 'user does not exist'}
                if not user.allowed(access_level):
                    return {'message': 'user do not have access to this section'}
            else:
                return {'message': 'user does not exist'}
            return f(*args, **kwargs)
        return decorated_function
    return decorator
