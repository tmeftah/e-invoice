from http import HTTPStatus

from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from webargs import fields
from webargs.flaskparser import use_kwargs

from app.main.models.users import ACCESS, UserModel
from app.main.resources import cache
from app.main.schemas.users import UserPaginationSchema, UserSchema
from app.main.users.decorators import requires_access_level
from app.main.utils import clear_cache

# -*- coding: utf-8 -*-


user_schema = UserSchema()
user_pagiantion_schema = UserPaginationSchema()


class UserList(Resource):

    # @requires_access_level(ACCESS['guest'])

    # @cache.cached(timeout=60, key_prefix=cache_json_keys)
    @use_kwargs({"q": fields.Str(missing=''),
                 "page": fields.Int(missing=1),
                 'per_page': fields.Int(missing=20),
                 'sort': fields.Str(missing='username'),
                 'order': fields.Str(missing='asc')}, location="query")  # set location to query for pagination
    @cache.cached(timeout=60, query_string=True)
    @jwt_required
    def get(self, q, page, per_page, sort, order, **kwargs):

        users = UserModel.get_all_published(
            q, page, per_page, sort, order)
        return user_pagiantion_schema.dump(users)

    def post(self):
        json_data = request.get_json()
        schema = UserSchema(exclude=("hyperlink",))
        try:
            data = schema.load(json_data)
        except ValidationError as err:
            return err.messages

        if UserModel.find_by_username(data.get("username")):
            return {'message': "User already exists. Please Log in.",
                    'status': 'fail'}, HTTPStatus.BAD_REQUEST

        try:
            new_user = UserModel(
                username=data.get('username'),
                password=UserModel.generate_hash(data['password']), access=0)

            new_user.save_to_db()
            clear_cache('/users')
            return UserSchema().dump(new_user), HTTPStatus.CREATED

        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, HTTPStatus.INTERNAL_SERVER_ERROR


class User(Resource):

   # @jwt_required
   # @requires_access_level(ACCESS['user'])
    @cache.cached(timeout=60, query_string=True)
    @jwt_required
    def get(self, id):
        user = UserModel.find_by_id(id)
        if not user:
            return {'message': 'no user found'}, HTTPStatus.NOT_FOUND

        return user_schema.dump(user), HTTPStatus.OK

    @jwt_required
    def put(self, id):

        json_data = request.get_json()
        try:
            data = user_schema.load(data=json_data, partial=('username',))
        except ValidationError as err:
            return err.messages

        user = UserModel.find_by_id(id)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        user.password = UserModel.generate_hash(
            data.get('password')) or user.password

        if current_user.is_admin():
            user.access = ACCESS[data.get('access')] or user.access

        user.save_to_db()

        clear_cache('/users')

        return user_schema.dump(user), HTTPStatus.OK

    @jwt_required
    def delete(self, id):

        user = UserModel.find_by_id(id=id)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        user.delete_from_db()

        clear_cache('/users')

        return {}, HTTPStatus.NO_CONTENT
