from http import HTTPStatus

import marshmallow as ma
from flask import request
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from sqlalchemy import exists, func

from src.auth.entities import User
from src.customer.entrypoints.flask.response_utils import (
    create_response_error,
    create_validation_error,
)
from src.db import session_factory


class LoginSchema(ma.Schema):
    email = ma.fields.Email(required=True)
    password = ma.fields.String(required=True)


def email_already_registered(session, email):
    where_condition = func.lower(User.email) == func.lower(email)
    stmt = exists().where(where_condition)
    return session.query(stmt).scalar()


def get_user(session, email):
    return (
        session.query(User)
        .filter(func.lower(User.email) == func.lower(email))
        .one_or_none()
    )


@doc(tags=['auth'])
class SignUpView(MethodResource):
    @use_kwargs(LoginSchema, apply=False)
    @marshal_with('', code=HTTPStatus.OK, apply=False)
    @marshal_with('', code=HTTPStatus.NOT_FOUND, apply=False)
    def post(self):
        try:
            request_data = LoginSchema().load(request.json)
        except ValidationError as err:
            return create_validation_error(err)

        email = request_data.get('email')
        session = session_factory()

        if email_already_registered(session, email):
            return create_response_error(
                code='EMAIL_ALREADY_REGISTERED',
                message=f'Email "{email}" already registered',
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        user = User.create(email=email, password=request_data.get('password'))
        session.add(user)
        session.commit()

        return {'message': 'User registered with success'}, HTTPStatus.CREATED


@doc(tags=['auth'])
class LoginView(MethodResource):
    @use_kwargs(LoginSchema, apply=False)
    @marshal_with('', code=HTTPStatus.OK, apply=False)
    @marshal_with('', code=HTTPStatus.UNAUTHORIZED, apply=False)
    def post(self):
        try:
            request_data = LoginSchema().load(request.json)
        except ValidationError as err:
            return create_validation_error(err)

        email = request_data.get('email', None)
        password = request_data.get('password', None)

        session = session_factory()
        user = get_user(session, email)

        if not user or not user.check_password(password):
            return create_response_error(
                code='AUTHENTICATION_FAILED',
                message='Wrong email or password',
                status_code=HTTPStatus.UNAUTHORIZED,
            )

        return {'token': create_access_token(identity=email)}, HTTPStatus.OK
