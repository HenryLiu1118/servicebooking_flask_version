from flask_restful import Resource, reqparse
from flask import jsonify, g
from middleware.auth import token_required, authorize
from db import db
from models.language import Language
from models.servicetype import ServiceType
from models.role import Role
from models.user import User


class AdminLanguage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name')

    @token_required
    @authorize('Admin')
    def get(self):
        return [language.json() for language in Language.query.order_by(Language.id).all()]

    @token_required
    @authorize('Admin')
    def post(self):
        data = AdminLanguage.parser.parse_args()
        errors = []
        if data['name'] is None:
            errors.append('Please include name')

        if len(errors) != 0:
            return {'errors': errors}, 400

        language = Language.find_by_name(data['name'])
        if language:
            return {'error': 'Lanugage already exists'}, 400

        language = Language(data['name'])

        db.session.add(language)
        db.session.commit()

        return language


class AdminRole(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name')

    @token_required
    @authorize('Admin')
    def get(self):
        return [role.json() for role in Role.query.order_by(Role.id).all()]

    @token_required
    @authorize('Admin')
    def post(self):
        data = AdminLanguage.parser.parse_args()
        errors = []
        if data['name'] is None:
            errors.append('Please include name')

        if len(errors) != 0:
            return {'errors': errors}, 400

        role = Role.find_by_name(data['name'])
        if role:
            return {'error': 'Rolename  already exists'}, 400

        role = Role(data['name'])

        db.session.add(role)
        db.session.commit()

        return role


class AdminServiceType(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name')

    @token_required
    @authorize('Admin')
    def get(self):
        return list(map(lambda x: x.json(), ServiceType.query.order_by(ServiceType.id).all()))

    @token_required
    @authorize('Admin')
    def post(self):
        data = AdminLanguage.parser.parse_args()
        errors = []
        if data['name'] is None:
            errors.append('Please include name')

        if len(errors) != 0:
            return {'errors': errors}, 400

        serviceType = ServiceType.find_by_name(data['name'])
        if serviceType:
            return {'error': 'Service already exists'}, 400

        serviceType = ServiceType(data['name'])

        db.session.add(serviceType)
        db.session.commit()

        return serviceType


class AdminUser(Resource):
    @token_required
    @authorize('Admin')
    def get(self):
        return jsonify([item.json() for item in User.query.order_by(User.id).all()])
