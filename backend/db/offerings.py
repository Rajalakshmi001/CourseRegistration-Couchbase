from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
from couchbase.result import SubdocResult
import couchbase.subdocument as subdoc
from adb_utils import catch_missing, require_json_data, catch_already_exists, json_response, flatten_subdoc_result
from db.quarters import quarterPut as upsert_quarter, quarterGet as get_for_quarter

offering_bucket = cluster.open_bucket('offerings')


@catch_missing
def offering_main(quarterId, courseId, sectionId):
    method_map = {"GET": offeringGet, "PUT": offeringPut, "POST": offeringPost, "DELETE": offeringDelete}
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
    

def all_offerings():
    all_nested = list(quarter['offerings'] for quarter in offering_bucket.n1ql_query('select * from offerings'))
    
    
    return json_response(flatten_subdoc_result(all_nested, 2)) 

def __offering_lookup_helper(qId, path):
    ob_data = offering_bucket.lookup_in(qId, subdoc.get(path))  # type: SubdocResult
    return ob_data[0]

def get_course_sections(quarterId, courseId):
    return json_response(list(__offering_lookup_helper(quarterId, courseId).values()))

def get_single_offering(quarterId, courseId, sectionId):
    return json_response(__offering_lookup_helper(quarterId, courseId+'.'+sectionId))


@require_json_data
@catch_already_exists
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
