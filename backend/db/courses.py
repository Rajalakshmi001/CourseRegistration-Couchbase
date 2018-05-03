from flask import Flask, request, Response, json, make_response
import db.couchbase_server as cbs
from adb_utils import catch_missing, require_json_data, catch_already_exists, json_response

course_bucket = cbs.Buckets.course_bucket

@catch_missing
def course_main(courseId):
    method_map = {"GET": courseGET, "PUT": coursePUT, "POST": coursePOST, "DELETE": courseDELETE}
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for courses".format(request.method))
    
    f = method_map[request.method]
    
    return f(courseId)


def courseGET(courseId):
    if not courseId:
        # return all courseId
        return json_response(list(course['courses'] for course in course_bucket.n1ql_query('select * from courses')))

    return json_response(course_bucket.get(courseId, quiet=True).value)


@catch_already_exists
def coursePUT(courseId):
    data = request.get_json()
    course_bucket.insert(courseId, request.get_json())  # type: OperationResult
    return make_response('Course ' + courseId + ' inserted', 201)


def coursePOST(courseId):
    data = request.get_json()
    opres = course_bucket.replace(courseId, request.get_json())  # type: OperationResult
    return make_response('Course updated: ' + opres.success, 200)


def courseDELETE(courseId):
    # TODO: delete all offerings
    del_res = course_bucket.remove(courseId)  # type: OperationResult
    return make_response("Successfully deleted" if del_res.success else "Delete failed")
