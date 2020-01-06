from flask import request, jsonify, make_response, g
from models.servicetype import ServiceType
from models.language import Language
from functools import wraps


def filterResult(model):
    def filterResult_decordator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            page = int(request.args['page']) if 'page' in request.args else 0
            limit = int(request.args['limit']) if 'limit' in request.args else 2

            serviceName = kwargs['serviceName'] if 'serviceName' in kwargs else None
            languageName = kwargs['languageName'] if 'languageName' in kwargs else None
            serviceType, language = None, None

            if serviceName:
                serviceType = ServiceType.find_by_name(serviceName)
                if not serviceType:
                    return make_response(jsonify({'error': 'Service Type does not exists'}), 400)

            if languageName:
                language = Language.find_by_name(languageName)
                if not language:
                    return make_response(jsonify({'error': 'language does not exists'}), 400)

            if serviceName and languageName:
                allModel = [item.json() for item in
                            model.filter_by_service_language(service_type_id=serviceType.id, language_id=language.id)]
            elif languageName:
                allModel = [item.json() for item in model.filter_by_language(language_id=language.id)]
            elif serviceName:
                allModel = [item.json() for item in model.filter_by_service(service_type_id=serviceType.id)]
            else:
                allModel = [item.json() for item in model.query.all()]

            returnModels = allModel[page * limit: page * limit + limit]

            if model.__tablename__ == 'request_order':
                g.res = jsonify({
                    'requestDtoList': returnModels,
                    'size': len(allModel)
                })
            else:
                g.res = jsonify({
                    'serviceDtoList': returnModels,
                    'size': len(allModel)
                })

            return f(*args, **kwargs)

        return decorated
    return filterResult_decordator
