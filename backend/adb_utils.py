import functools
import json
from flask import make_response, request, Response
from couchbase.exceptions import NotFoundError, KeyExistsError, SubdocPathNotFoundError, SubdocPathExistsError

def catch404(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (NotFoundError, SubdocPathNotFoundError) as err:
            return make_response("for {} {}, {} not found".format(request.method, function.__name__, err.key), 204)
    
    return wrapper


def catch_already_exists(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (KeyExistsError, SubdocPathExistsError) as kee:
            kee.key
            return make_response('{} already existed; not modified'.format(kee.key), 304)
    
    return wrapper


def require_json_data(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if not request.get_json():
            return make_response("No data supplied", 400)
        return function(*args, **kwargs)
    
    return wrapper
    

def json_response(data, code=200):
    return Response(response=json.dumps(data), status=code, mimetype='application/json')

