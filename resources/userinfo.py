import datetime
from flask_restful import Resource, reqparse
from middleware.auth import token_required
from flask import g
from models.language import Language
from db import db
arguments = ['firstname', 'lastname', 'streetname', 'city', 'state', 'zipcode', 'phone', 'language']


class UserInfo(Resource):
    parser = reqparse.RequestParser()
    for argument in arguments:
        parser.add_argument(argument)

    @token_required
    def put(self):
        data = UserInfo.parser.parse_args()
        errors = []
        for argument in arguments:
            if data[argument] is None:
                errors.append(f"Please include {argument}")

        if len(errors) != 0:
            return {'errors': errors}, 400

        language = Language.find_by_name(data['language'])
        if not language:
            return {'error': 'Language doesn\'t exist'}, 400

        user = g.current_user
        user.update_at = datetime.datetime.now()
        user.UserInfo.firstname = data['firstname']
        user.UserInfo.lastname = data['lastname']
        user.UserInfo.streetname = data['streetname']
        user.UserInfo.city = data['city']
        user.UserInfo.state = data['state']
        user.UserInfo.zipcode = data['zipcode']
        user.UserInfo.phone = data['phone']

        pastLanguage = user.UserInfo.Language.name

        # To be updated
        if pastLanguage != language:
            pass

        user.UserInfo.Language = language

        db.session.add(user)
        db.session.commit()

        return user.json()


class UserInfoMine(Resource):
    @token_required
    def get(self):
        user = g.current_user
        if not user:
            return {'error', 'Invalid Credentials'}, 400
        return user.json()


