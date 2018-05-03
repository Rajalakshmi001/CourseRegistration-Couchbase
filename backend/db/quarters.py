from flask import Flask, request, Response, json, make_response
import db.couchbase_server as cbs
import couchbase.subdocument as subdoc 
from adb_utils import catch_missing, require_json_data, catch_already_exists, json_response

offering_bucket = cbs.Buckets.offering_bucket


@catch_missing
def quarter_main(quarterId):
    method_map = {"GET": quarterGet, "DELETE": quarterDelete}
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for quarters".format(request.method))
    
    return method_map[request.method](quarterId)


@catch_already_exists
def quarterPut(quarterId):
    offering_bucket.insert(quarterId, {})  # upsert would wipe
    return make_response("Created quarter", 200)


def quarterGet(quarterId):
    all_nested = offering_bucket.get(quarterId, quiet=True).value
    if not all_nested:
        return json_response(None)

    flat = []
    for values in ((list(value.values()) for value in all_nested.values())):
        flat.extend(values)

    return json_response(flat) 


def quarterDelete(quarterId):
    offering_bucket.remove(quarterId)
    return make_response("Deleted")
