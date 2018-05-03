from flask import Flask, request, Response, json, make_response
import db.couchbase_server as cbs
from couchbase.result import SubdocResult
import couchbase.subdocument as subdoc
from adb_utils import catch_missing, require_json_data, catch_already_exists, json_response, flatten_subdoc_result, pull_flask_args
from db.quarters import quarterPut as upsert_quarter, quarterGet as get_for_quarter

offering_bucket = cbs.Buckets.offering_bucket


@catch_missing
@pull_flask_args
def offering_main(quarter, courseNum, offeringId):
    method_map = {"GET": offeringGET, "PUT": offeringPUT, "POST": offeringPOST, "DELETE": offeringDELETE}
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for offerings".format(request.method))

    return method_map[request.method](quarter, courseNum, offeringId)


def offeringGET(quarter, courseNum, sectionId):
    if not sectionId:
        if not courseNum:
            if not quarter:
                return json_response(all_offerings())
            return get_for_quarter(quarter)
        return json_response(get_course_sections(quarter, courseNum))
    return json_response(get_single_offering(quarter, courseNum, sectionId))
    
def all_offerings():
    all_nested = list(quarter['offerings'] for quarter in offering_bucket.n1ql_query('select * from offerings'))    
    return flatten_subdoc_result(all_nested, 2)

def __offering_lookup_helper(qId, path):
    ob_data = offering_bucket.lookup_in(qId, subdoc.get(path))  # type: SubdocResult
    return ob_data[0]

def get_course_sections(quarter, courseNum):
    return list(__offering_lookup_helper(quarter, courseNum).values())

def get_single_offering(quarter, courseNum, sectionId):
    return __offering_lookup_helper(quarter, courseNum+'.'+sectionId)


@catch_already_exists
def offeringPUT(quarter, courseNum, sectionId):
    # TODO: make redis call
    if not (quarter and courseNum and sectionId):
        return make_response("Missing a parameter. Need quarter, courseNum, sectionId", 400)
    upsert_quarter(quarter)
    data = request.get_json()
    data['enrolled'] = 0
    data['capacity'] = int(data['capacity']) if 'capacity' in data else 0
    offering_bucket.mutate_in(quarter, subdoc.insert(courseNum+"."+str(sectionId), data, create_parents=True))
    return make_response("Created offering {}/{}-{}".format(quarter, courseNum, sectionId), 201)


def offeringPOST(quarter, courseNum, sectionId):
    # TODO: make redis call
    if not (quarter and courseNum and sectionId):
        return make_response("Missing a parameter. Need quarter, courseNum, sectionId", 400)
    offering_bucket.mutate_in(quarter, subdoc.replace(courseNum+"."+sectionId, request.get_json()))
    return make_response("Updated offering {}/{}-{}".format(quarter, courseNum, sectionId), 200)


def offeringDELETE(quarter, courseNum, sectionId):
    # TODO: make redis call
    sec = ("." + sectionId) if sectionId else ''
    offering_bucket.mutate_in(quarter, subdoc.remove(courseNum + sec))
    return make_response("Deleted", 200)


def get_available_spots(quarterId, courseNum, offeringId):
    offering = get_single_offering(quarterId, courseNum, offeringId)
    return offering['capacity']  - offering['enrolled']


def change_enrollment_count(quarterId, courseNum, offeringId, delta):
    return list(offering_bucket.mutate_in(quarterId, subdoc.counter(courseNum+'.'+offeringId+'.enrolled', delta)))[0]


def incr_enrollment_count(quarterId, courseNum, offeringId):
    return change_enrollment_count(quarterId, courseNum, offeringId, 1)


def decr_enrollment_count(quarterId, courseNum, offeringId):
    return change_enrollment_count(quarterId, courseNum, offeringId, -1)


def zero_enrollment_count(quarterId, courseNum, offeringId):
    return list(offering_bucket.mutate_in(quarterId, subdoc.upsert(courseNum+'.'+offeringId+'.enrolled', 0)))[0]
