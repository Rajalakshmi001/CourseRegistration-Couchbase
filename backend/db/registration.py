from flask import Flask, request, Response, json
import db.couchbase_server as cb
import couchbase.subdocument as subdoc 
from couchbase.result import SubdocResult
from couchbase.exceptions import SubdocPathNotFoundError, NotFoundError, TimeoutError
from adb_utils import pull_flask_args, catch_missing, require_json_data, catch_already_exists, json_response, log_make_response
import db.users
import db.offerings as offerings
import db.schedules
from db.poly_publisher import Neo4JPublisher

offering_bucket = cb.Buckets.offering_bucket
sched_bucket = cb.Buckets.schedule_bucket


def register_main(studentId, quarterId, courseNum, offeringId):
    method_map = {"PUT": registerPUT, "DELETE": registerDELETE}
    
    if not (studentId and quarterId and courseNum and offeringId):
        return log_make_response("Missing a param", 400)

    return method_map[request.method](studentId, quarterId, courseNum, offeringId)


def registerPUT(studentId, quarterId, courseNum, offeringId):
    sched_key = studentId+"-"+quarterId
    # verify that offering is real
    try:
        offering = list(offering_bucket.lookup_in(quarterId, subdoc.get(courseNum+'.'+offeringId)))[0]
    except (SubdocPathNotFoundError, NotFoundError):
        return log_make_response("Offering does not exist", 400)
    
    # verify that student is real
    try:
        assert db.users.get_user(studentId)
    except:
        return log_make_response("User {} does not exist".format(studentId), 400)
    
    # see if student is already enrolled
    try:
        sched = db.schedules.get_user_schedule(studentId, quarterId)
        assert sched is None or courseNum not in sched['offerings'] 
        print("User is not already enrolled in course")
    except AssertionError:
        return log_make_response("User already enrolled in course", 304)  # type: Response
    except NotFoundError:
        pass

    num_enrolled = offering['enrolled']
    capacity = offering['capacity']
    if num_enrolled >= capacity:
        return log_make_response("Class is full/maximum capacity reached", 403)
    
    # make user's schedule entry for that quarter if it doesn't exist
    db.schedules.initialize_user_schedule(studentId, quarterId)

    # try:
        # sched_bucket.insert(sched_key, {"studentId": studentId, "quarterId": quarterId})
    # except:
        # pass

    db.schedules.add_course_to_sched(studentId, quarterId, courseNum, offeringId)
    data = { 'studentId': studentId, 'quarterId': quarterId, 'courseNum': courseNum, 'offeringId': offeringId }
    incr = offering_bucket.mutate_in(quarterId, subdoc.counter(courseNum+'.'+offeringId+'.enrolled', 1))
    print("Incremented enrollment count to:", list(incr)[0])
    Neo4JPublisher().create_enrollment(data)
    return log_make_response("Registered {} for {}: {}-{}".format(studentId, quarterId, courseNum, offeringId), 201)


@catch_missing
def registerDELETE(studentId, quarterId, courseNum, offeringId):
    class_str = "{}: {}-{}".format(quarterId, courseNum, offeringId)
    try:
        unregister(studentId, quarterId, courseNum, offeringId)
    except SubdocPathNotFoundError:
        return log_make_response(studentId + " was not registered for " + class_str, 400)
    return log_make_response("Un-registered "+studentId+ " from "+class_str)


def unregister(studentId, quarterId, courseNum, offeringId):
    # sched_bucket.mutate_in(studentId+"-"+quarterId, subdoc.remove('offerings.'+courseNum))  # will throw exception if user is not registered for course
    db.schedules.remove_course_from_sched(studentId, quarterId, courseNum, offeringId)
    ## decr = list(offering_bucket.mutate_in(quarterId, subdoc.counter(courseNum+'.'+offeringId+'.enrolled', -1)))[0]
    decr = offerings.decr_enrollment_count(quarterId, courseNum, offeringId)
    print("Decremented enrollment count to:", decr)
    if decr < 0:
        zero_res = offerings.zero_enrollment_count(quarterId, courseNum, offeringId)
        print("Reset to zero:", zero_res)

    return True
