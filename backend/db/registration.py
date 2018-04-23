from flask import Flask, request, Response, json


def register_main(userId, offeringId):
    method_map = {"GET": registerGet, "PUT": registerPut, "POST": registerPost, "DELETE": registerDelete}
    print(request.method, userId, offeringId)
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for registrations".format(request.method))
    
    return method_map[request.method](userId, offeringId)


def registerGet(userId, offeringId):
    return "You tried to register '{}' for '{}', but this endpoint is not actually implemented yet".format(userId, offeringId)


def registerPut(userId, offeringId):
    return Response(response=json.dumps(request.get_json()), status=200, mimetype='application/json')


def registerPost(userId, offeringId):
    pass


def registerDelete(userId, offeringId):
    pass
