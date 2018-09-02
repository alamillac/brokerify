from flask import session, request
from flask_restful import Resource
from app.models.core import User
from web.api.forms import LoginForm
from web.api.serializer import UserSchema
from functools import wraps


user_schema = UserSchema()


def valid_user(username, password):
    #TODO validate password
    user = User.get(username)
    return user


def login_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'username' not in session:
            return {"error": "Login required"}, 401 # TODO formatear errores {"status": "fail", "message": "Login required", "error_code": XXX}, 401
        return func(*args, **kwargs)
    return decorator


class Login(Resource):
    def post(self):
        data = request.get_json() or {}
        result = LoginForm().load(data)
        if result.errors:
            return {"error": "Invalid data", "fields": result.errors}, 400

        login_data = result.data
        user = valid_user(login_data['username'], login_data['password'])
        if not user:
            return {"error": "Invalid username or password"}, 401

        session['username'] = login_data['username']
        response = user_schema.dump(user)
        return response.data, 200
