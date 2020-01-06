from flask_restful import Resource, reqparse
from middleware.auth import token_required, authorize
from middleware.filterresult import filterResult
from flask import g
from models.servicetype import ServiceType
from models.serviceprovide import ServiceProvide
from db import db

arguments = ['detail', 'price', 'servicename']


class AllProvide(Resource):
    @token_required
    @authorize('Customer')
    def get(self):
        return filterResult(ServiceProvide)


class ProvideByService(Resource):
    @token_required
    @authorize('Customer')
    def get(self, serviceName):
        return filterResult(model=ServiceProvide, serviceName=serviceName)


class ProvideByLanguage(Resource):
    @token_required
    @authorize('Customer')
    def get(self, languageName):
        return filterResult(model=ServiceProvide, languageName=languageName)


class ProvideByServiceAndLanguage(Resource):
    @token_required
    @authorize('Customer')
    def get(self, serviceName, languageName):
        return filterResult(model=ServiceProvide, serviceName=serviceName, languageName=languageName)


class MyProvide(Resource):
    @token_required
    @authorize('Service')
    def get(self):
        user = g.current_user
        serviceProvide = user.ServiceProvide
        return serviceProvide.json()


class UpdateProvide(Resource):
    parser = reqparse.RequestParser()
    for argument in arguments:
        parser.add_argument(argument)

    @token_required
    @authorize('Service')
    def post(self):
        data = UpdateProvide.parser.parse_args()
        errors = []
        for argument in arguments:
            if data[argument] is None:
                errors.append(f"Please include {argument}")

        if len(errors) != 0:
            return {'errors': errors}, 400

        serviceType = ServiceType.find_by_name(data['servicename'])
        if not serviceType:
            return {'error': 'Service doesn\'t exist'}, 400

        user = g.current_user
        serviceProvide = user.ServiceProvide

        if not serviceProvide:
            serviceProvide = ServiceProvide(data['detail'], data['price'])

        serviceProvide.detail = data['detail']
        serviceProvide.price = data['price']
        serviceProvide.ServiceType = serviceType
        serviceProvide.Language = user.UserInfo.Language

        db.session.add(serviceProvide)
        db.session.commit()

        return serviceProvide.json()
