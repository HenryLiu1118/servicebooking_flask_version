import datetime
from flask_restful import Resource, reqparse
from middleware.auth import token_required, authorize
from middleware.filterresult import filterResult
from flask import g, request, jsonify
from models.requestorder import RequestOrder
from db import db
from models.servicetype import ServiceType

arguments = ['info', 'servicetype']


class AllRequest(Resource):
    @token_required
    @authorize('Service')
    def get(self):
        return filterResult(RequestOrder)


class MyRequest(Resource):
    @token_required
    @authorize('Customer')
    def get(self):
        page = int(request.args['page']) if 'page' in request.args else 0
        limit = int(request.args['limit']) if 'limit' in request.args else 2

        allRequestOrder = [item.json() for item in RequestOrder.filter_by_user_id(g.current_user.id)]
        requestOrders = allRequestOrder[page * limit: page * limit + limit]

        return jsonify({
            'returnModels': requestOrders,
            'size': len(allRequestOrder)
        })


class RequestByService(Resource):
    @token_required
    @authorize('Service')
    def get(self, serviceName):
        return filterResult(model=RequestOrder, serviceName=serviceName)


class RequestByLanguage(Resource):
    @token_required
    @authorize('Service')
    def get(self, languageName):
        return filterResult(model=RequestOrder, languageName=languageName)


class RequestItem(Resource):
    @token_required
    def get(self, RequestId):
        return jsonify(RequestOrder.find_by_id(RequestId=RequestId).json())


class RequestByServiceAndLanguage(Resource):
    @token_required
    @authorize('Service')
    def get(self, serviceName, languageName):
        return filterResult(model=RequestOrder, serviceName=serviceName, languageName=languageName)


class RequestDeleteAndUpdate(Resource):
    parser = reqparse.RequestParser()
    for argument in arguments:
        parser.add_argument(argument)

    @token_required
    @authorize('Customer')
    def delete(self, RequestId):
        requestOrder = RequestOrder.find_by_id(RequestId=RequestId)
        if not requestOrder:
            return {'error': 'requestOrder doesn\'t exist'}, 400

        requestUser = requestOrder.User
        user = g.current_user

        if requestUser.id != user.id:
            return {'error': 'RequestOrder is not yours!'}, 400

        db.session.delete(requestOrder)
        db.session.commit()

        return {'message': 'delete successfully!'}

    @token_required
    @authorize('Customer')
    def put(self, RequestId):
        data = RequestDeleteAndUpdate.parser.parse_args()
        errors = []
        for argument in arguments:
            if data[argument] is None:
                errors.append(f"Please include {argument}")

        if len(errors) != 0:
            return {'errors': errors}, 400

        serviceType = ServiceType.find_by_name(data['servicetype'])
        if not serviceType:
            return {'error': 'Service doesn\'t exist'}, 400

        requestOrder = RequestOrder.find_by_id(RequestId=RequestId)
        if not requestOrder:
            return {'error': 'requestOrder doesn\'t exist'}, 400

        requestUser = requestOrder.User
        user = g.current_user

        if requestUser.id != user.id:
            return {'error': 'RequestOrder is not yours!'}, 400

        requestOrder.info = data['info']
        requestOrder.update_at = datetime.datetime.now()
        requestOrder.ServiceType = serviceType

        db.session.add(requestOrder)
        db.session.commit()

        return jsonify(requestOrder.json())


class PostRequest(Resource):
    parser = reqparse.RequestParser()
    for argument in arguments:
        parser.add_argument(argument)

    @token_required
    @authorize('Customer')
    def post(self):
        data = PostRequest.parser.parse_args()
        errors = []
        for argument in arguments:
            if data[argument] is None:
                errors.append(f"Please include {argument}")

        if len(errors) != 0:
            return {'errors': errors}, 400

        serviceType = ServiceType.find_by_name(data['servicetype'])
        if not serviceType:
            return {'error': 'Service doesn\'t exist'}, 400

        user = g.current_user
        requestOrder = RequestOrder(data['info'], True)
        requestOrder.create_at = datetime.datetime.now()
        requestOrder.User = user
        requestOrder.Language = user.UserInfo.Language
        requestOrder.ServiceType = serviceType

        db.session.add(requestOrder)
        db.session.commit()

        return jsonify(requestOrder.json())
