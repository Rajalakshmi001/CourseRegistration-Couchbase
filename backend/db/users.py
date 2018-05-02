from flask import Flask, request, Response, json, make_response
import db.couchbase_server as cb
from adb_utils import catch_missing, catch_already_exists, json_response, pull_flask_args
from db.schedules import del_all_scheds_for

user_bucket = cb.cluster.open_bucket('users')
sched_bucket = cb.cluster.open_bucket('schedules')

@pull_flask_args
def user_main(username):
    method_map = {"GET": userGet, "PUT": userPut, "POST": userPost, "DELETE": userDelete}
    try:
        return method_map[request.method](username)
    except AssertionError:
        return make_response("Must include username", 400)

def userGet(username):
    if not username:
        # return all users
        return json_response(list(user_bucket.n1ql_query('select username,name from users')))
    
    return json_response(get_user(username))  # type: ValueResult
    

def get_user(username):
    return user_bucket.get(username, quiet=True).value


@catch_already_exists
def userPut(username):
    data = request.get_json()
    user_bucket.insert(username, data)  # type: OperationResult
    return make_response('User ' + username + ' inserted', 201)


@catch_missing
def userPost(username):
    data = request.get_json()
    opres = user_bucket.replace(username, data)  # type: OperationResult
    return make_response('Document updated: ' + opres.success, 200)
 

@catch_missing
def userDelete(username):
    del_res = user_bucket.remove(username)  # type: OperationResult
    del_all_scheds_for(username)
    return make_response('Deletion value {}, success {}'.format(del_res.value, del_res.success))
