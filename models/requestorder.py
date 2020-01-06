from db import db


class RequestOrder(db.Model):
    __tablename__ = 'request_order'

    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(80))
    active = db.Column(db.Boolean)
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    User = db.relationship('User')

    service_type_id = db.Column(db.Integer, db.ForeignKey('service_type.id'))
    ServiceType = db.relationship('ServiceType')

    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    Language = db.relationship('Language')

    Comment = db.relationship('Comment')

    def json(self):
        return {
            'requestId': self.id,
            'servicetype': self.ServiceType.name,
            'info': self.info,
            'active': self.active,
            'userDto': self.User.json(),
            'create_At': self.create_at,
            'update_At': self.update_at
        }

    def __init__(self, info, active):
        self.info = info
        self.active = active

    @classmethod
    def find_by_id(cls, RequestId):
        return cls.query.filter_by(id=RequestId).first()

    @classmethod
    def filter_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def filter_by_language(cls, language_id):
        return cls.query.filter_by(language_id=language_id)

    @classmethod
    def filter_by_service(cls, service_type_id):
        return cls.query.filter_by(service_type_id=service_type_id)

    @classmethod
    def filter_by_service_language(cls, service_type_id, language_id):
        return cls.query.filter_by(language_id=language_id, service_type_id=service_type_id)