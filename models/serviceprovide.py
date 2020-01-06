from db import db


class ServiceProvide(db.Model):
    __tablename__ = 'service_provide'

    id = db.Column(db.Integer, primary_key=True)
    detail = db.Column(db.String(80))
    price = db.Column(db.String(80))

    User = db.relationship('User', uselist=False)

    service_type_id = db.Column(db.Integer, db.ForeignKey('service_type.id'))
    ServiceType = db.relationship('ServiceType')

    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    Language = db.relationship('Language')

    def json(self):
        user = self.User
        return {
            'serviceId': self.id,
            'detail': self.detail,
            'price': self.price,
            'servicetype': self.ServiceType.name,
            'userDto': user.json()
        }

    def __init__(self, detail, price):
        self.detail = detail
        self.price = price

    @classmethod
    def filter_by_language(cls, language_id):
        return cls.query.filter_by(language_id=language_id)

    @classmethod
    def filter_by_service(cls, service_type_id):
        return cls.query.filter_by(service_type_id=service_type_id)

    @classmethod
    def filter_by_service_language(cls, service_type_id, language_id):
        return cls.query.filter_by(language_id=language_id, service_type_id=service_type_id)
