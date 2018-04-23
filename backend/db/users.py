from flask import Flask, request, Response, json


def user_main(userId):
    method_map = {"GET": userGet, "PUT": userPut, "POST": userPost, "DELETE": userDelete}
    print(request.method, userId)
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for users".format(request.method))
    
    return method_map[request.method](userId)


def userGet(userId):
    return "You requested user '{}', but this endpoint is not actually implemented yet".format(userId)

def userPut(userId):
    pass

def userPost(userId):
    pass

def userDelete(userId):
    pass