from flask import Flask, request, Response, json
from db.couchbase_server import *
import couchbase.subdocument as subdoc 
from adb_utils import catch404, require_json_data, catch_already_exists, json_response

offering_bucket = cluster.open_bucket('offerings')


@catch404
def quarter_main(quarterId):
    method_map = {"GET": quarterGet, "DELETE": quarterDelete}
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for quarters".format(request.method))
    
    return method_map[request.method](quarterId)


@catch_already_exists
def quarterPut(quarterId):
    offering_bucket.insert(quarterId, {})  # upsert would wipe


def quarterGet(quarterId):
    return json_response(offering_bucket.get(quarterId, silent=True)) 


def quarterDelete(quarterId):
    pass
