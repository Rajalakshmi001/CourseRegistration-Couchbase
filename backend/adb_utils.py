import functools
import traceback
import inspect
import json
from flask import make_response, request, Response
from couchbase.exceptions import NotFoundError, KeyExistsError, SubdocPathNotFoundError, SubdocPathExistsError, TimeoutError
from db.couchbase_server import Buckets

def catch_missing(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (NotFoundError, SubdocPathNotFoundError):
            return json_response(None, 200)
    
    return wrapper


def catch_already_exists(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (KeyExistsError, SubdocPathExistsError) as kee:
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


def flatten_subdoc_result(lod, levels=2):
  if not (levels):
    return lod
  
  one_flatter = []
  for d in lod:
    one_flatter.extend(d.values())
    
  return flatten_subdoc_result(one_flatter, levels-1)


def pull_flask_args(function):
    arg_names = inspect.getfullargspec(function).args
    @functools.wraps(function)
    def wrapper(*args, **kwargs):   
        req_data = (request.data and request.get_json()) or dict()
        ad = dict(zip(arg_names, args))
        def __get(dictionary, key):
            return dictionary[key] if key in dictionary else None
        def val(key):
            return __get(req_data, key) or __get(kwargs, key) or __get(ad, key) or None
        new_kwa = {key: val(key) for key in arg_names}
        print()
        print(request.method, request.url, new_kwa) 
        if request.method in ['PUT', 'POST']:
            for arg in arg_names:
                if arg not in req_data:
                    return make_response("Missing '{}' for {}".format(arg, request.method), 400)
        return function(**new_kwa)
    return wrapper


def log_make_response(*args, **kwargs):
    resp = make_response(*args, **kwargs)  # type: Response
    print(resp.status_code, resp.get_data(True))
    return resp


def catch_return_exceptions(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except TimeoutError as e:
            print(dict(type=str(e.__class__.__name__), message=str(e)))
            return json_response("Timed out (> {} s) on {} {}\n{}".format(Buckets._timeout, request.method, request.url, e), 504)
        except Exception as e:
            trace = traceback.format_exc()
            d = dict(type=str(e.__class__.__name__), message=str(e), stack=trace)
            print(trace)
            return json_response(d, 500)
    return wrapper
