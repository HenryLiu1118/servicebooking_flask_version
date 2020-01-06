from db import db


class UserInfo(db.Model):
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    streetname = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    zipcode = db.Column(db.String(80))
    phone = db.Column(db.String(80))

    User = db.relationship('User')

    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    Language = db.relationship('Language')

    def json(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'streetname': self.streetname,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode,
            'phone': self.phone
        }