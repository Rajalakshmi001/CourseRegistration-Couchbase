from flask import Flask, request, Response, json


def quarter_main(quarterId):
    method_map = {"GET": quarterGet, "PUT": quarterPut, "POST": quarterPost, "DELETE": quarterDelete}
    print(request.method, quarterId)
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for quarters".format(request.method))
    
    return method_map[request.method](quarterId)


def quarterGet(quarterId):
    return "You requested quarter '{}', but this endpoint is not actually implemented yet".format(quarterId)


def quarterPut(quarterId):
    return Response(response=json.dumps(request.get_json()), status=200, mimetype='application/json')


def quarterPost(quarterId):
    pass


def quarterDelete(quarterId):
    pass
