import functools
from flask import make_response, request
from couchbase.exceptions import NotFoundError

def catch404(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except NotFoundError as nfe:
            return make_response("for {} {}, {} not found".format(request.method, function.__name__, nfe.key), 404)
    
    return wrapper


def require_json_data(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if not request.get_json():
            return make_response("No data supplied", 400)
        return function(*args, **kwargs)
    
    return wrapper
    