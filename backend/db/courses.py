from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
from utils import catch404, require_json_data, catch_already_exists

course_bucket = cluster.open_bucket('courses')


@catch404
def course_main(courseId):
    method_map = {"GET": courseGet, "PUT": coursePut, "POST": coursePost, "DELETE": courseDelete}
    print(request.method, courseId)
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for courses".format(request.method))
    
    f = method_map[request.method]
    
    return f(courseId)


def courseGet(courseId):
    if not courseId:
        # return all courseId
        return Response(response=json.dumps(list(course['courses'] for course in course_bucket.n1ql_query('select * from courses'))), status=200, mimetype='application/json')

    cb_data = course_bucket.get(courseId)  # type: ValueResult
    return Response(response=json.dumps(cb_data.value), status=200, mimetype='application/json')


@require_json_data
@catch_already_exists
def coursePut(courseId):
    data = request.get_json()
    course_bucket.insert(courseId, request.get_json())  # type: OperationResult
    return make_response('Document ' + courseId + ' inserted', 200)


@require_json_data
def coursePost(courseId):
    data = request.get_json()
    opres = course_bucket.replace(courseId, request.get_json())  # type: OperationResult
    return make_response('Document updated: ' + opres.success, 200)


def courseDelete(courseId):
    del_res = course_bucket.remove(courseId)  # type: OperationResult
    return make_response("Successfully deleted" if del_res.success else "Delete failed")
