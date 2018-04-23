from flask import Flask, request, Response, json


def professor_main(professorId):
    method_map = {"GET": professorGet, "PUT": professorPut, "POST": professorPost, "DELETE": professorDelete}
    print(request.method, professorId)
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for professors".format(request.method))
    
    return method_map[request.method](professorId)


def professorGet(professorId):
    return "You requested professor '{}', but this endpoint is not actually implemented yet".format(professorId)


def professorPut(professorId):
    return Response(response=json.dumps(request.get_json()), status=200, mimetype='application/json')


def professorPost(professorId):
    pass


def professorDelete(professorId):
    pass
