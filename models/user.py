from db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    user_info_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    UserInfo = db.relationship('UserInfo', uselist=False)

    serviceprovide_id = db.Column(db.Integer, db.ForeignKey('service_provide.id'))
    ServiceProvide = db.relationship('ServiceProvide', uselist=False)

    Role = db.relationship('Role')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    RequestOrder = db.relationship('RequestOrder')
    Comment = db.relationship('Comment')

    def json(self):
        userinfo = self.UserInfo
        return {
            'userId': self.id,
            'username': self.username,
            'firstname': userinfo.firstname,
            'lastname': userinfo.lastname,
            'streetname': userinfo.streetname,
            'city': userinfo.city,
            'state': userinfo.state,
            'zipcode': userinfo.zipcode,
            'phone': userinfo.phone,
            'language': userinfo.Language.name,
            'role': self.Role.name
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
