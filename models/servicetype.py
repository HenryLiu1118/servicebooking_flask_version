from db import db


class ServiceType(db.Model):
    __tablename__ = 'service_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    ServiceProvide = db.relationship('ServiceProvide')
    RequestOrder = db.relationship('RequestOrder')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()