from flask import Flask, request, Response, json


def course_main(courseId):
    method_map = {"GET": courseGet, "PUT": coursePut, "POST": coursePost, "DELETE": courseDelete}
    print(request.method, courseId)
    if request.method not in method_map:
        raise NotImplementedError("Method {} not implemented for courses".format(request.method))
    
    return method_map[request.method](courseId)


def courseGet(courseId):
    return "You requested course '{}', but this endpoint is not actually implemented yet".format(courseId)


def coursePut(courseId):
    return Response(response=json.dumps(request.get_json()), status=200, mimetype='application/json')


def coursePost(courseId):
    pass


def courseDelete(courseId):
    pass
