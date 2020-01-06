from functools import wraps
from flask import request, jsonify, g, make_response
import jwt
from models.user import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization'] if 'Authorization' in request.headers else None

        if not token:
            return make_response(jsonify({'error': 'No Token Found'}), 401)

        try:
            data = jwt.decode(token, 'henrySecretToken', algorithms='HS256')
            g.current_user = User.find_by_id(data['id'])
        except:
            return make_response(jsonify({'error': 'Token is inValid'}), 401)

        return f(*args, **kwargs)

    return decorated


def authorize(role):
    def authorize_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            r = g.current_user.Role.name
            if r != role:
                return make_response(jsonify({'error': f'{r} is not authorized to access this route'}), 401)
            return f(*args, **kwargs)

        return decorated

    return authorize_decorator
