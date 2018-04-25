from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
import couchbase.subdocument as subdoc 
from couchbase.result import SubdocResult
from utils import catch404, require_json_data, catch_already_exists

offering_bucket = cluster.open_bucket('offerings')


@catch404
def offering_main(quarterId, courseId, sectionId):
    method_map = {"GET": offeringGet, "PUT": offeringPut, "POST": offeringPost, "DELETE": offeringDelete}
    print(request.method, quarterId, courseId, sectionId)
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for offerings".format(request.method))
    
    return method_map[request.method](quarterId, courseId, sectionId)


def offeringGet(quarterId, courseId, sectionId):
    ob_data = offering_bucket.lookup_in(quarterId, subdoc.get(courseId+("."+sectionId if int(sectionId) else "")))  # type: SubdocResult
    
    return Response(response=json.dumps(list(ob_data)[0]), status=200, mimetype='application/json')


@require_json_data
def offeringPut(quarterId, courseId, sectionId):
    @catch_already_exists
    def mquarter():
        offering_bucket.insert(quarterId, {})
    mquarter()

    offering_bucket.mutate_in(quarterId, subdoc.insert(courseId+"."+sectionId, request.get_json(), create_parents=True))
    return make_response("Created offering {}/{}-{}".format(quarterId, courseId, sectionId), 200)


def offeringPost(quarterId, courseId, sectionId):
    offering_bucket.mutate_in(quarterId, subdoc.replace(courseId+"."+sectionId, request.get_json()))
    return make_response("Updated offering {}/{}-{}".format(quarterId, courseId, sectionId), 200)


def offeringDelete(quarterId, courseId, sectionId):
    pass
