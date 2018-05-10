from flask import Flask, request, Response, json, Blueprint, send_from_directory, make_response
from flask_server.crossorigin import crossdomain
from db import courses,users,offerings,quarters,registration,schedules,search,recommendations
from adb_utils import catch_return_exceptions, json_response, catch_missing, pull_flask_args


app = Flask(__name__)

ALL_METHODS = ['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS']
GET,PUT,POST,DELETE,OPTIONS = ALL_METHODS


@app.route('/')
@crossdomain(origin='*', methods=['GET'], headers=['content-type'])
@catch_return_exceptions
def hello():
    return 'root'


@app.route('/user', methods=ALL_METHODS)
@app.route('/users', methods=['GET', 'OPTIONS'])  # to get all users. Same as GET /user
@app.route('/user/<username>', methods=['GET', 'PUT', 'POST' , 'DELETE' , 'OPTIONS'])  # TODO: remove PUT
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], headers=['content-type'])
@catch_return_exceptions
def user(username=None):
    return users.user_main(username)

@app.route('/professors', methods=['GET', 'OPTIONS']) 
@crossdomain(origin='*', methods=['GET', 'OPTIONS'], headers=['content-type'])
@catch_return_exceptions
def professors():
    return json_response(users.get_professors())


@app.route('/students', methods=['GET', 'OPTIONS']) 
@crossdomain(origin='*', methods=['GET', 'OPTIONS'], headers=['content-type'])
@catch_return_exceptions
def students():
    return json_response(users.get_students())


@app.route('/course', methods=ALL_METHODS)
@app.route('/courses', methods=['GET'])  # to get all courses. Same as GET /course
@app.route('/course/<courseId>', methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS'])  # TODO: remove PUT
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], headers=['content-type'])
@catch_return_exceptions
def course(courseId=None):
    return courses.course_main(courseId)


@app.route('/offering', methods=ALL_METHODS)  # all offerings
@app.route('/offerings', methods=[GET])  # same as above
@app.route('/offering/<quarter>', methods=['GET'])  # all offerings for a quarter
@app.route('/offerings/<quarter>', methods=['GET'])  # same as above
@app.route('/offering/<quarter>/<courseNum>', methods=[GET, DELETE])  # all offerings for a course in a quarter
@app.route('/offerings/<quarter>/<courseNum>', methods=[GET, DELETE])  # same as above
@app.route('/offering/<quarter>/<courseNum>/<offeringId>', methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS'])  # specific offering
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], headers=['content-type'])
@catch_return_exceptions
def offering(quarter=None, courseNum=None, offeringId=None):
    return offerings.offering_main(quarter, courseNum, offeringId)


@app.route('/quarter/<quarterId>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'], headers=['content-type'])
@catch_return_exceptions
def quarter(quarterId=None):
    return quarters.quarter_main(quarterId)


@app.route('/recommend/<userId>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'OPTIONS'], headers=['content-type'])
@catch_return_exceptions
def getRecommendations(userId):
    return recommendations.recommend_main(userId)


@app.route('/register', methods=['PUT', 'DELETE', 'OPTIONS'])
@app.route('/register/<userId>/<quarterId>/<courseNum>/<offeringId>', methods=['PUT', 'DELETE', 'OPTIONS'])
@crossdomain(origin='*', methods=['PUT', 'DELETE', 'OPTIONS'], headers=['content-type'])
@catch_return_exceptions
@catch_missing
@pull_flask_args
def registerForCourse(studentId=None, quarterId=None, courseNum=None, offeringId=None):
    return registration.register_main(studentId, quarterId, courseNum, offeringId)


@app.route('/lookup/<studentId>/<quarterId>', methods=['GET'])
@crossdomain(origin='*', methods=['GET', 'OPTIONS'], headers=['content-type'])
@catch_return_exceptions
def scheduleLookup(studentId, quarterId):
    try:
        return json_response(schedules.get_user_schedule(studentId, quarterId))
    except Exception as e:
        print("Lookup exception:", type(e), e)
        return make_response(str(e), 500)


@app.route('/generateSchedules/', methods=['POST'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
@catch_return_exceptions
def generateSchedules():
    pass


@app.route('/logs', methods=['GET'])
@crossdomain(origin='*', methods=['GET', 'OPTIONS'], headers=['content-type'])
@catch_return_exceptions
def getLogs():
    with open('adb.log', 'r') as log_file:
        return Response(response=log_file.read(), status=200)


@app.route('/search', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', methods=['POST', 'OPTIONS'], headers=['content-type'])
@catch_return_exceptions
def search_query():
    return json_response(search.run_search(**(request.get_json())))
    


if __name__ == '__main__':
    print("You are running flaskServer.py directly; it will probably fail. Use run.py instead.")
    app.run(host='0.0.0.0', port=5005)
