from flask import Flask, request, Response, json


def offering_main(offeringId):
    method_map = {"GET": offeringGet, "PUT": offeringPut, "POST": offeringPost, "DELETE": offeringDelete}
    print(request.method, offeringId)
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for offerings".format(request.method))
    
    return method_map[request.method](offeringId)


def offeringGet(offeringId):
    return "You requested offering '{}', but this endpoint is not actually implemented yet".format(offeringId)


def offeringPut(offeringId):
    return Response(response=json.dumps(request.get_json()), status=200, mimetype='application/json')


def offeringPost(offeringId):
    pass


def offeringDelete(offeringId):
    pass
