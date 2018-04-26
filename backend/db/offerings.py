from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
from couchbase.result import SubdocResult
from utils import catch404, require_json_data, catch_already_exists
from db.quarters import quarterPut as upsert_quarter, quarterGet as get_for_quarter

offering_bucket = cluster.open_bucket('offerings')


@catch404
def offering_main(quarterId, courseId, sectionId):
    method_map = {"GET": offeringGet, "PUT": offeringPut, "POST": offeringPost, "DELETE": offeringDelete}
    print(request.method, quarterId, courseId, sectionId)
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for offerings".format(request.method))
    
    return method_map[request.method](quarterId, courseId, sectionId)


def offeringGet(quarterId, courseId, sectionId):
    if not sectionId:
        if not courseId:
            if not quarterId:
                return all_offerings()
            return get_for_quarter(quarterId)
        return get_course_sections(quarterId, courseId)
    return get_single_offering(quarterId, courseId, sectionId)
    
    ob_data = offering_bucket.lookup_in(quarterId, subdoc.get(courseId+("" if not sectionId else '.'+sectionId)))  # type: SubdocResult
    return Response(response=json.dumps(list(ob_data)[0]), status=200, mimetype='application/json')

def all_offerings():
    # can I really do that? 
    return None

def __offering_lookup_helper(qId, path):
    ob_data = offering_bucket.lookup_in(qId, subdoc.get(path))  # type: SubdocResult
    return Response(response=json.dumps(list(ob_data)[0]), status=200, mimetype='application/json')

def get_course_sections(quarterId, courseId):
    return __offering_lookup_helper(quarterId, courseId)

def get_single_offering(quarterId, courseId, sectionId):
    return __offering_lookup_helper(quarterId, courseId+'.'+sectionId)


@require_json_data
def offeringPut(quarterId, courseId, sectionId):
    upsert_quarter(quarterId)
    offering_bucket.mutate_in(quarterId, subdoc.insert(courseId+"."+sectionId, request.get_json(), create_parents=True))
    return make_response("Created offering {}/{}-{}".format(quarterId, courseId, sectionId), 201)


def offeringPost(quarterId, courseId, sectionId):
    offering_bucket.mutate_in(quarterId, subdoc.replace(courseId+"."+sectionId, request.get_json()))
    return make_response("Updated offering {}/{}-{}".format(quarterId, courseId, sectionId), 200)


def offeringDelete(quarterId, courseId, sectionId):
    sec = ("." + sectionId) if sectionId else ''
    offering_bucket.mutate_in(quarterId, subdoc.remove(courseId + sec))
    return make_response("Deleted", 204)
