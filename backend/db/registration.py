from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
import couchbase.subdocument as subdoc 
from adb_utils import pull_flask_args, catch_missing, require_json_data, catch_already_exists, json_response, SubdocPathNotFoundError
from db.offerings import offeringGet

off_bucket = cluster.open_bucket('offerings')
sched_bucket = cluster.open_bucket('schedules')


@pull_flask_args
def register_main(studentId=None, quarterId=None, courseNum=None, offeringId=None):
    method_map = {"GET": registerGet, "PUT": registerPut, "DELETE": registerDelete}
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for registrations".format(request.method))
    
    # data = request.get_json() or request.headers
    # studentId = data['studentId']
    # quarterId = data['quarterId']
    # courseNum = data['courseNum']
    # offeringId = data['offeringId']
    print("in reg:", studentId, quarterId, courseNum, offeringId)

    if not (studentId and quarterId and courseNum and offeringId):
        return make_response("Missing a param")

    return method_map[request.method](studentId, quarterId, courseNum, offeringId)


@catch_missing
def registerGet(studentId, quarterId):    
    json_response(sched_bucket.get(studentId+'-'+quarterId, quiet=True).value)


@catch_already_exists
@catch_missing
def registerPut(studentId, quarterId, courseNum, offeringId):
    offering = json.loads(offeringGet(quarterId, courseNum, offeringId).get_data())
    num_enrolled = offering['enrolled']
    capacity = offering['capacity']
    if num_enrolled >= capacity:
        return make_response("Class is full/maximum capacity reached", 400)
    try:
        sched_bucket.insert(studentId+"-"+quarterId, {"studentId": studentId, "quarterId": quarterId})
    except:
        pass
    print(sched_bucket.mutate_in(studentId+"-"+quarterId, subdoc.insert('offerings.'+courseNum, offeringId, create_parents=True)))
    off_bucket.mutate_in(quarterId, subdoc.counter(courseNum+'.'+offeringId+'.enrolled', 1))
    return make_response("Registered {} for {}: {}-{}".format(studentId, quarterId, courseNum, offeringId), 201)


@catch_missing
def registerDelete(studentId, quarterId, courseNum, offeringId):
    try:
        sched_bucket.mutate_in(studentId+"-"+quarterId, subdoc.remove('offerings.'+courseNum))  # will throw exception if user is not registered for course
    except SubdocPathNotFoundError:
        return make_response("{} was not registered for {}: {}-{}".format(studentId, quarterId, courseNum, offeringId), 400)
    off_bucket.mutate_in(quarterId, subdoc.counter(courseNum+'.'+offeringId+'.enrolled', -1))
    return make_response("Un-registered {} from {}: {}".format(studentId, quarterId, courseNum))
