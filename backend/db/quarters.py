from flask import Flask, request, Response, json
from db.couchbase_server import *
import couchbase.subdocument as subdoc 
from utils import catch404, require_json_data, catch_already_exists

offering_bucket = cluster.open_bucket('offerings')


@catch404
def quarter_main(quarterId):
    method_map = {"GET": quarterGet, "PUT": quarterPut, "POST": quarterPost, "DELETE": quarterDelete}
    print(request.method, quarterId)
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for quarters".format(request.method))
    
    return method_map[request.method](quarterId)


def quarterGet(quarterId):
    qb_data = offering_bucket.get(quarterId)  # type: ValueResult
    return Response(response=json.dumps(qb_data.value), status=200, mimetype='application/json')


@catch_already_exists
def quarterPut(quarterId):

    return Response(response=json.dumps(request.get_json()), status=200, mimetype='application/json')


def quarterPost(quarterId):
    pass


def quarterDelete(quarterId):
    pass
