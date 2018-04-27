from flask import Flask, request, Response, json, make_response
import db.couchbase_server as cb
from adb_utils import catch_missing, require_json_data, catch_already_exists, json_response

user_bucket = cb.cluster.open_bucket('users')


@catch_missing
def user_main(userId):
    method_map = {"GET": userGet, "PUT": userPut, "POST": userPost, "DELETE": userDelete}
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for users".format(request.method))

    print(request.get_json())

    return method_map[request.method](userId)


def userGet(userId):
    if not userId:
        # return all users
        return json_response(list(user_bucket.n1ql_query('select username,name from users')))
    
    return json_response(user_bucket.get(userId, quiet=True).value)  # type: ValueResult
    

@require_json_data
@catch_already_exists
def userPut(userId):
    data = request.get_json()
    user_bucket.insert(userId, request.get_json())  # type: OperationResult
    return make_response('User ' + userId + ' inserted', 201)


def userPost(userId):
    data = request.get_json()
    opres = user_bucket.replace(userId, request.get_json())  # type: OperationResult
    return make_response('Document updated: ' + opres.success, 200)
 

def userDelete(userId):
    del_res = user_bucket.remove(userId)  # type: OperationResult
    return make_response('Deletion value {}, success {}'.format(del_res.value, del_res.success))