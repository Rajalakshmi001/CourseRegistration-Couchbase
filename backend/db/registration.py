from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
import couchbase.subdocument as subdoc 
from adb_utils import catch_missing, require_json_data, catch_already_exists, json_response, SubdocPathNotFoundError
from db.offerings import offeringGet

off_bucket = cluster.open_bucket('offerings')
sched_bucket = cluster.open_bucket('schedules')

def register_main():
    method_map = {"GET": registerGet, "PUT": registerPut, "DELETE": registerDelete}
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for registrations".format(request.method))
    
    data = request.get_json()
    if not data:
        data = request.headers
    userId = data['studentId']
    quarterId = data['quarterId']
    courseId = data['courseNum']
    sectionNum = data['offeringId']
    if not (userId and quarterId and courseId and sectionNum):
        raise ValueError("Missing param")

    return method_map[request.method](userId, quarterId, courseId, sectionNum)


@catch_missing
def registerGet(studentId, quarterId):
    return json_response(sched_bucket.get(studentId+'-'+quarterId, quiet=True).value)


@catch_already_exists
@catch_missing
def registerPut(userId, quarterId, courseId, sectionNum):
    offering = json.loads(offeringGet(quarterId, courseId, sectionNum).get_data())
    num_enrolled = offering['enrolled']
    capacity = offering['capacity']
    
    if num_enrolled >= capacity:
        return make_response("Class is full/maximum capacity reached", 400)

    try:
        sched_bucket.insert(userId+"-"+quarterId, {"studentId": userId, "quarterId": quarterId})
    except:
        pass
    print(sched_bucket.mutate_in(userId+"-"+quarterId, subdoc.insert('offerings.'+courseId, sectionNum, create_parents=True)))

    print(off_bucket.mutate_in(quarterId, subdoc.counter(courseId+'.'+sectionNum+'.enrolled', 1)))

    return make_response("Registered {} for {}: {}-{}".format(userId, quarterId, courseId, sectionNum), 201)


@catch_missing
def registerDelete(userId, quarterId, courseId, offeringId):
    try:
        sched_bucket.mutate_in(userId+"-"+quarterId, subdoc.remove('offerings.'+courseId))  # will throw exception if user is not registered for course
    except SubdocPathNotFoundError:
        return make_response("{} was not registered for {}: {}-{}".format(userId, quarterId, courseId, offeringId), 400)
    off_bucket.mutate_in(quarterId, subdoc.counter(courseId+'.'+offeringId+'.enrolled', -1))
    return make_response("Un-registered {} from {}: {}".format(userId, quarterId, courseId))
