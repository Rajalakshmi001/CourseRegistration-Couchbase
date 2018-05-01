from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
import couchbase.subdocument as subdoc 
from couchbase.exceptions import SubdocPathNotFoundError, NotFoundError
from adb_utils import pull_flask_args, catch_missing, require_json_data, catch_already_exists, json_response
from db.offerings import offeringGet
from db.users import get_user

off_bucket = cluster.open_bucket('offerings')
sched_bucket = cluster.open_bucket('schedules')


@pull_flask_args
def register_main(studentId=None, quarterId=None, courseNum=None, offeringId=None):
    method_map = {"PUT": registerPut, "DELETE": registerDelete}
    
    if not (studentId and quarterId and courseNum and offeringId):
        return make_response("Missing a param", 400)

    return method_map[request.method](studentId, quarterId, courseNum, offeringId)


# @catch_already_exists
# @catch_missing
def registerPut(studentId, quarterId, courseNum, offeringId):
    # get offering
    try:
        offering = off_bucket.lookup_in(quarterId, subdoc.get(courseNum+'.'+offeringId))
    except (SubdocPathNotFoundError, NotFoundError) as err:
        return make_response("Offering does not exist", 400)

    # get student
    try:
        assert get_user(userId)
    except:
        return make_response("User does not exist", 400)

    num_enrolled = offering['enrolled']
    capacity = offering['capacity']
    if num_enrolled >= capacity:
        return make_response("Class is full/maximum capacity reached", 400)
    
    # make schedule entry if it doesn't exist
    try:
        sched_bucket.insert(studentId+"-"+quarterId, {"studentId": studentId, "quarterId": quarterId})
    except:
        pass
    sched_bucket.mutate_in(studentId+"-"+quarterId, subdoc.insert('offerings.'+courseNum, offeringId, create_parents=True))
    print("here", off_bucket.mutate_in(quarterId, subdoc.counter(courseNum+'.'+offeringId+'.enrolled', 1)))
    return make_response("Registered {} for {}: {}-{}".format(studentId, quarterId, courseNum, offeringId), 201)


@catch_missing
def registerDelete(studentId, quarterId, courseNum, offeringId):
    class_str = "{}: {}-{}".format(quarterId, courseNum, offeringId)
    try:
        sched_bucket.mutate_in(studentId+"-"+quarterId, subdoc.remove('offerings.'+courseNum))  # will throw exception if user is not registered for course
    except SubdocPathNotFoundError:
        return make_response(studentId + " was not registered for " + class_str, 400)
    off_bucket.mutate_in(quarterId, subdoc.counter(courseNum+'.'+offeringId+'.enrolled', -1))
    return make_response("Un-registered "+studentId+ " from "+class_str)
