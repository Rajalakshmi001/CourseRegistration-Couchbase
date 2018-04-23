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
    opres = course_bucket.upsert(courseId, request.get_json())  # type: OperationResult
    print(opres, opres.success, opres.value)
    return make_response('Document inserted/updated', 200)
    # return Response(response=json.dumps(request.get_json()), status=200, mimetype='application/json')


def coursePost(courseId):
    pass


def courseDelete(courseId):
    del_res = course_bucket.remove(courseId)  # type: OperationResult
    print(del_res.value)
    return make_response('Deletion value {}, success {}'.format(del_res.value, del_res.success))
