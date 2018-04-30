import functools
import json
from flask import make_response, request, Response
from couchbase.exceptions import NotFoundError, KeyExistsError, SubdocPathNotFoundError, SubdocPathExistsError

def catch_missing(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (NotFoundError, SubdocPathNotFoundError) as err:
            return json_response(None, 200)
    
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


def flatten_subdoc_result(lod, levels=2):
  if not (levels):
    return lod
  
  one_flatter = []
  for d in lod:
    one_flatter.extend(d.values())
    
  return flatten_subdoc_result(one_flatter, levels-1)
  