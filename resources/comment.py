from flask_restful import Resource, reqparse
from flask import g, jsonify, make_response
from middleware.auth import token_required, authorize
from models.requestorder import RequestOrder
from models.comment import Comment
from db import db


class PostComment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('detail')

    @token_required
    @authorize('Service')
    def post(self, RequestOrderId):
        data = PostComment.parser.parse_args()
        errors = []
        if data['detail'] is None:
            errors.append('Please include your username')

        if len(errors) != 0:
            return {'errors': errors}, 400

        requestOrder = RequestOrder.find_by_id(RequestOrderId)
        user = g.current_user
        comment = Comment.find_by_userId_and_requestId(user_id=user.id, request_order_id=requestOrder.id)
        if comment:
            return {'error': 'You have already comment this Request!'}, 400

        comment = Comment(data['detail'])
        comment.RequestOrder = requestOrder
        comment.User = user

        db.session.add(comment)
        db.session.commit()

        return comment.json()


class Comments(Resource):
    @token_required
    def get(self, RequestOrderId):
        requestOrder = RequestOrder.find_by_id(RequestOrderId)
        user = g.current_user
        requestUser = requestOrder.User

        if user.id != requestUser.id:
            return {'error': 'RequestOrder is not yours!'}, 400

        allComments = requestOrder.Comment
        return make_response(jsonify([item.json() for item in allComments]), 200)


def findCommentById(CommentId, user):
    comment = Comment.find_by_id(commentId=CommentId)
    if not comment:
        return None

    requestOrder = comment.RequestOrder
    requestOrderUser = requestOrder.User
    commentUser = comment.User
    if user.id != commentUser.id and user.id != requestOrderUser.id:
        return None

    return comment


class CommentItem(Resource):
    @token_required
    def get(self, CommentId):
        comment = findCommentById(CommentId=CommentId, user=g.current_user)

        if not comment:
            return {'error': 'You cannot view this comment or this comment does not exists'}, 400

        return comment.json()

    @token_required
    def delete(self, CommentId):
        comment = findCommentById(CommentId=CommentId, user=g.current_user)
        if not comment:
            return {'error': 'You cannot view this comment or this comment does not exists'}, 400

        db.session.delete(comment)
        db.session.commit()

        return {'message': 'delete successfully!'}, 201


class CheckComment(Resource):
    @token_required
    @authorize('Service')
    def get(self, RequestOrderId):
        user = g.current_user
        comment = Comment.find_by_userId_and_requestId(user.id, RequestOrderId)

        if not comment:
            return jsonify(None)

        return jsonify(comment.json())

