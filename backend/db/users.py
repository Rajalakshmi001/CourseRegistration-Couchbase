from flask import Flask, request, Response, json, make_response
import db.couchbase_server as cb
from adb_utils import catch_missing, catch_already_exists, json_response, pull_flask_args
from db.schedules import del_all_scheds_for

user_bucket = cb.Buckets.user_bucket


@pull_flask_args
def user_main(username):
    method_map = {"GET": userGET, "PUT": userPUT, "POST": userPOST, "DELETE": userDELETE}
    try:
        return method_map[request.method](username)
    except AssertionError:
        return make_response("Must include username", 400)

def userGET(username):
    if not username:
        # return all users
       return json_response(get_all_users())
    
    return json_response(get_user(username))  # type: ValueResult


def get_user(username):
    return user_bucket.get(username, quiet=True).value


def get_all_users():
    return list(user_bucket.n1ql_query('select username,name,type from users'))


def get_students():
    return get_users_of_type('stud')

def get_professors():
    return get_users_of_type('prof')

def get_users_of_type(type):
    return list(user_bucket.n1ql_query("SELECT username,name FROM users WHERE type = '{}'".format(type)))


@catch_already_exists
def userPUT(username):
    data = request.get_json()
    user_bucket.insert(username, data)  # type: OperationResult
    return make_response('User ' + username + ' inserted', 201)


@catch_missing
def userPOST(username):
    data = request.get_json()
    opres = user_bucket.replace(username, data)  # type: OperationResult
    return make_response('Document updated: ' + opres.success, 200)
 

@catch_missing
def userDELETE(username):
    del_res = user_bucket.remove(username)  # type: OperationResult
    del_all_scheds_for(username)
    return json_response(del_res.success)
