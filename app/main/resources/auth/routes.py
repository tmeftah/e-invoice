import datetime
from http import HTTPStatus

from flask import current_app
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, get_raw_jwt,
                                jwt_refresh_token_required, jwt_required)
from flask_restful import Resource, reqparse

from app.main.models.users import UserModel
from app.main.resources.auth.exceptions_list import TokenNotFound
from app.main.resources.auth.jwt import (add_token_to_database,
                                         get_user_tokens, revoke_token,
                                         unrevoke_token)

parser_auth = reqparse.RequestParser()
parser_auth.add_argument(
    'username', help='This field cannot be blank', required=True)
parser_auth.add_argument(
    'password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):

    def post(self):

        data = parser_auth.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'User already exists. Please Log in.', 'status': 'fail'}, 409
        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password']),
            access=0
        )
        try:
            new_user.save_to_db()
            # access_token = create_access_token(identity=data['username'])
            # refresh_token = create_refresh_token(identity=data['username'])
            return {'message': 'User {} was created'.format(data['username']), 'status': 'success'
                    # 'access_token': access_token,
                    # 'refresh_token': refresh_token
                    }, HTTPStatus.CREATED
        except:
            return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR


class UserLogin(Resource):
    def post(self):
        data = parser_auth.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, HTTPStatus.UNAUTHORIZED

        if UserModel.verify_hash(data['password'], current_user.password):
            # Create our JWTs
            access_token = create_access_token(
                identity=data['username'], expires_delta=current_app.config["TOKEN_TIMEOUT"])
            refresh_token = create_refresh_token(identity=data['username'])

            # Store the tokens in our store with a status of not currently revoked.
            add_token_to_database(
                access_token, current_app.config['JWT_IDENTITY_CLAIM'])
            add_token_to_database(
                refresh_token, current_app.config['JWT_IDENTITY_CLAIM'])

            return {'user': {"username": current_user.username},
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }
        else:
            return {'message': 'Wrong credentials'}, HTTPStatus.UNAUTHORIZED
        # return {'message': 'User login'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        # Do the same thing that we did in the login endpoint here
        current_user = get_jwt_identity()
        access_token = create_access_token(
            identity=current_user, expires_delta=current_app.config["TOKEN_TIMEOUT"])
        add_token_to_database(
            access_token, current_app.config['JWT_IDENTITY_CLAIM'])
        return {'access_token': access_token}, HTTPStatus.CREATED


class GetTokenList(Resource):

    @jwt_required
    def get(self):
        def to_json(token):
            return {
                'id': token.id,
                'jti': token.jti,
                'token_type': token.token_type,
                'revoked': token.revoked,
                'expires': token.expires.strftime("%Y-%m-%d %H:%M:%S")
            }
        user_identity = get_jwt_identity()
        all_tokens = get_user_tokens(user_identity)

        return {'tokens': list(map(lambda token: to_json(token), all_tokens))}


class ModifyToken(Resource):
    @jwt_required
    def put(self, token_id):
        # Get and verify the desired revoked status from the body
        parser = reqparse.RequestParser()
        parser.add_argument(
            'revoke', type=bool, help='This field cannot be blank', required=True)
        data = parser.parse_args()
        revoke = data['revoke']
        # Revoke or unrevoke the token based on what was passed to this function
        user_identity = get_jwt_identity()
        try:
            if revoke:
                revoke_token(token_id, user_identity)
                return {'msg': 'Token revoked'}
            else:
                unrevoke_token(token_id, user_identity)
                return {'msg': 'Token unrevoked'}
        except TokenNotFound:
            return {'msg': 'The specified token was not found'},  HTTPStatus.NOT_FOUND


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'},  HTTPStatus.INTERNAL_SERVER_ERROR


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR
