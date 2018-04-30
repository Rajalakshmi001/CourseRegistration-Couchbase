from flask import Flask, request, Response, json
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


def registerPut(userId, quarterId, courseId, sectionNum):
    print("Registering {} to {}:{}-{}".format(userId, quarterId, courseId, sectionNum))
    # add to /offerings
    # off_bucket.mutate_in(quarterId, subdoc.array_addunique('.'.join((courseId, sectionNum, 'registrations')), userId, create_parents=True))

    # add to /schedules
    # return Response(response=json.dumps(request.get_json()), status=200, mimetype='application/json')
    try:
        sched_bucket.insert(userId+"-"+quarterId, {})
    except:
        pass
    sched_bucket.mutate_in(userId+"-"+quarterId, subdoc.upsert('offerings.'+courseId, sectionNum, create_parents=True))


def registerPost(userId, quarterId, courseId, sectionNum):
    pass


def registerDelete(userId, quarterId, courseId, sectionNum):
    pass
