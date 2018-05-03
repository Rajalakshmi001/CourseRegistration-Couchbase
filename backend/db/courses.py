from flask import Flask, request, Response, json, make_response
import db.couchbase_server as cbs
from adb_utils import catch_missing, require_json_data, catch_already_exists, json_response, pull_flask_args
from db.poly_publisher import RedisPublisher

course_bucket = cbs.Buckets.course_bucket

@catch_missing
@pull_flask_args
def course_main(courseNum):
    method_map = {"GET": courseGET, "PUT": coursePUT, "POST": coursePOST, "DELETE": courseDELETE}
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for courses".format(request.method))
    
    f = method_map[request.method]
    
    return f(courseNum)


def courseGET(courseNum):
    if not courseNum:
        # return all courseNum
        return json_response(list(course['courses'] for course in course_bucket.n1ql_query('select * from courses')))

    return json_response(course_bucket.get(courseNum, quiet=True).value)


@catch_already_exists
def coursePUT(courseNum):
    data = request.get_json()
    course_bucket.insert(courseNum, data)  # type: OperationResult
    RedisPublisher().create_course(data)
    return make_response('Course ' + courseNum + ' inserted', 201)


def coursePOST(courseNum):
    data = request.get_json()
    opres = course_bucket.replace(courseNum, request.get_json())  # type: OperationResult
    return make_response('Course updated: ' + opres.success, 200)


def courseDELETE(courseNum):
    # TODO: delete all offerings
    del_res = course_bucket.remove(courseNum)  # type: OperationResult
    RedisPublisher().delete_course(dict(courseNum=courseNum))
    return make_response("Successfully deleted" if del_res.success else "Delete failed")
