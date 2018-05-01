from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
from couchbase.result import SubdocResult
import couchbase.subdocument as subdoc
from adb_utils import catch_missing, require_json_data, catch_already_exists, json_response, flatten_subdoc_result, pull_flask_args
from db.quarters import quarterPut as upsert_quarter, quarterGet as get_for_quarter

offering_bucket = cluster.open_bucket('offerings')


@catch_missing
@pull_flask_args
def offering_main(quarter, courseNum, offeringId):
    method_map = {"GET": offeringGet, "PUT": offeringPut, "POST": offeringPost, "DELETE": offeringDelete}
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for offerings".format(request.method))

    return method_map[request.method](quarter, courseNum, offeringId)


def offeringGet(quarter, courseNum, sectionId):
    if not sectionId:
        if not courseNum:
            if not quarter:
                return all_offerings()
            return get_for_quarter(quarter)
        return get_course_sections(quarter, courseNum)
    return get_single_offering(quarter, courseNum, sectionId)
    
def all_offerings():
    all_nested = list(quarter['offerings'] for quarter in offering_bucket.n1ql_query('select * from offerings'))    
    return json_response(flatten_subdoc_result(all_nested, 2)) 

def __offering_lookup_helper(qId, path):
    ob_data = offering_bucket.lookup_in(qId, subdoc.get(path))  # type: SubdocResult
    return ob_data[0]

def get_course_sections(quarter, courseNum):
    return json_response(list(__offering_lookup_helper(quarter, courseNum).values()))

def get_single_offering(quarter, courseNum, sectionId):
    return json_response(__offering_lookup_helper(quarter, courseNum+'.'+sectionId))


@catch_already_exists
def offeringPut(quarter, courseNum, sectionId):
    if not (quarter and courseNum and sectionId):
        return make_response("Missing a parameter. Need quarter, courseNum, sectionId", 400)
    upsert_quarter(quarter)
    data = request.get_json()
    data['enrolled'] = 0
    data['capacity'] = int(data['capacity']) if 'capacity' in data else 0
    offering_bucket.mutate_in(quarter, subdoc.insert(courseNum+"."+sectionId, data, create_parents=True))
    return make_response("Created offering {}/{}-{}".format(quarter, courseNum, sectionId), 201)


def offeringPost(quarter, courseNum, sectionId):
    if not (quarter and courseNum and sectionId):
        return make_response("Missing a parameter. Need quarter, courseNum, sectionId", 400)
    offering_bucket.mutate_in(quarter, subdoc.replace(courseNum+"."+sectionId, request.get_json()))
    return make_response("Updated offering {}/{}-{}".format(quarter, courseNum, sectionId), 200)


def offeringDelete(quarter, courseNum, sectionId):
    sec = ("." + sectionId) if sectionId else ''
    offering_bucket.mutate_in(quarter, subdoc.remove(courseNum + sec))
    return make_response("Deleted", 200)
