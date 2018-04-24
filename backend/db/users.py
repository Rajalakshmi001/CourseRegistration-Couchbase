from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
from utils import catch404, require_json_data

user_bucket = cluster.open_bucket('users')


@catch404
def user_main(userId):
    method_map = {"GET": userGet, "PUT": userPut, "POST": userPost, "DELETE": userDelete}
    print(request.method, userId)
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for users".format(request.method))
    
    return method_map[request.method](userId)


def userGet(userId):
    ub_data = user_bucket.get(userId)  # type: ValueResult
    return Response(response=json.dumps(ub_data.value), status=200, mimetype='application/json')
    

@require_json_data
def userPut(userId):
    data = request.get_json()
    try:
        user_bucket.insert(userId, request.get_json())  # type: OperationResult
        return make_response('User ' + userId + ' inserted', 200)
    except KeyExistsError:
        return make_response('User ' + userId + ' already existed', 400)


def userPost(userId):
    data = request.get_json()
    opres = user_bucket.replace(userId, request.get_json())  # type: OperationResult
    return make_response('Document updated: ' + opres.success, 200)
 

def userDelete(userId):
    del_res = user_bucket.remove(userId)  # type: OperationResult
    return make_response('Deletion value {}, success {}'.format(del_res.value, del_res.success))