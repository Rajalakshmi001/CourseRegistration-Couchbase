from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
import couchbase.subdocument as subdoc 
from adb_utils import catch_missing, require_json_data, catch_already_exists, json_response

off_bucket = cluster.open_bucket('offerings')
sched_bucket = cluster.open_bucket('schedules')

def register_main():
    method_map = {"GET": registerGet, "PUT": registerPut, "POST": registerPost, "DELETE": registerDelete}
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


def registerGet(userId, quarterId, courseId, *a, **kw):
    pass


@catch_already_exists
def registerPut(userId, quarterId, courseId, sectionNum):
    try:
        sched_bucket.insert(userId+"-"+quarterId, {"studentId": userId, "quarterId": quarterId})
    except:
        pass
    sched_bucket.mutate_in(userId+"-"+quarterId, subdoc.insert('offerings.'+courseId, sectionNum, create_parents=True))
    return make_response("Registered {} for {}: {}-{}".format(userId, quarterId, courseId, sectionNum))


def registerPost(userId, quarterId, courseId, sectionNum):
    pass


def registerDelete(userId, quarterId, courseId, sectionNum):
    pass
