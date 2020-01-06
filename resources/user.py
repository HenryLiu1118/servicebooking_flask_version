from flask_restful import Resource, reqparse
from flask_bcrypt import Bcrypt
import jwt
import datetime
from models.user import User
from models.userinfo import UserInfo
from models.language import Language
from models.role import Role
from models.servicetype import ServiceType
from db import db
from middleware.auth import token_required

arguments = ['username', 'password', 'firstname', 'lastname', 'streetname', 'city', 'state', 'zipcode', 'phone', 'role',
             'language']
bcrypt = Bcrypt()


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')

    def post(self):
        data = UserLogin.parser.parse_args()
        errors = []
        if data['username'] is None:
            errors.append('Please include your username')
        if data['password'] is None:
            errors.append('Please include your password')

        if len(errors) != 0:
            return {'errors': errors}, 400

        user = User.find_by_username(data['username'])

        if not user or not bcrypt.check_password_hash(user.password, data['password']):
            return {'error': 'Invalid Credentials'}, 400

        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'henrySecretToken', algorithm='HS256')

        return {
            'token': token.decode('UTF-8'),
            'user': user.json()
        }


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    for argument in arguments:
        parser.add_argument(argument)

    def post(self):
        data = UserRegister.parser.parse_args()
        errors = []
        for argument in arguments:
            if data[argument] is None:
                errors.append(f"Please include {argument}")

        if len(errors) != 0:
            return {'errors': errors}, 400

        if User.find_by_username(data['username']):
            return {'error': 'User already existed!'}, 400

        language = Language.find_by_name(data['language'])
        if not language:
            return {'error': 'Language doesn\'t exist'}, 400
        role = Role.find_by_name(data['role'])
        if not role:
            return {'error': 'Role doesn\'t exist'}, 400

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        userinfo = UserInfo(firstname=data['firstname'],
                            lastname=data['lastname'],
                            streetname=data['streetname'],
                            city=data['city'],
                            state=data['state'],
                            zipcode=data['zipcode'],
                            phone=data['phone'],
                            language_id=language.id)

        user = User(username=data['username'],
                    password=hashed_password,
                    create_at=datetime.datetime.now(),
                    role_id=role.id)

        user.UserInfo = userinfo

        db.session.add(user)
        db.session.commit()

        return {'message': 'User Registered!'}, 201


class UserRole(Resource):
    @token_required
    def get(self):
        return [role.json() for role in Role.query.all() if role.name != 'Admin']


class UserServiceType(Resource):
    @token_required
    def get(self):
        return list(map(lambda x: x.json(), ServiceType.query.all()))


class UserLanguage(Resource):
    @token_required
    def get(self):
        return [language.json() for language in Language.query.all()]
