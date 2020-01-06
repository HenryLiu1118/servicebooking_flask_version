from db import db


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    detail = db.Column(db.String(80))

    request_order_id = db.Column(db.Integer, db.ForeignKey('request_order.id'))
    RequestOrder = db.relationship('RequestOrder')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    User = db.relationship('User')

    def json(self):
        requestOrder = self.RequestOrder
        user = self.User.json()
        requestOrderUser = requestOrder.User.json()
        serviceType = requestOrder.ServiceType.json()
        return {
            'commentId': self.id,
            'commentDetail': self.detail,
            'servicetype':serviceType,
            'info': requestOrder.info,
            'active': requestOrder.active,
            'requestUser': requestOrderUser,
            'userdto': user
        }

    def __init__(self, detail):
        self.detail = detail

    @classmethod
    def find_by_id(cls, commentId):
        return cls.query.filter_by(id=commentId).first()

    @classmethod
    def find_by_userId_and_requestId(cls, user_id, request_order_id):
        return cls.query.filter_by(user_id=user_id, request_order_id=request_order_id).first()
