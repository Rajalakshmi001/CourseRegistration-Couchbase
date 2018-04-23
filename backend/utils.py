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