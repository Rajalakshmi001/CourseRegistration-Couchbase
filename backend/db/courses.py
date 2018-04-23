from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
from utils import catch404

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
    cb_data = course_bucket.get(courseId)  # type: ValueResult
    return Response(response=json.dumps(cb_data.value), status=200, mimetype='application/json')


def coursePut(courseId):
    data = request.get_json()
    if not data:
        return make_response("No data supplied", 400)
    try:
        course_bucket.insert(courseId, request.get_json())  # type: OperationResult
        return make_response('Document ' + courseId + ' inserted', 200)
    except KeyExistsError:
        return make_response('Document ' + courseId + ' already existed', 400)


def coursePost(courseId):
    data = request.get_json()
    if not data:
        return make_response("No data supplied", 400)
    opres = course_bucket.replace(courseId, request.get_json())
    return make_response('Document updated', 200)


def courseDelete(courseId):
    del_res = course_bucket.remove(courseId)  # type: OperationResult
    print(del_res.value)
    return make_response('Deletion value {}, success {}'.format(del_res.value, del_res.success))
