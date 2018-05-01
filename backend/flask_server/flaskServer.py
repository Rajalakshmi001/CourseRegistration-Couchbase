from flask import Flask, request, Response, json, Blueprint, send_from_directory
from flask_server.crossorigin import crossdomain
from db import courses,users,offerings,quarters,professors,registration


app = Flask(__name__)

ALL_METHODS = ['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS']
GET,PUT,POST,DELETE,OPTIONS = ALL_METHODS


@app.route('/')
@crossdomain(origin='*', methods=['GET'], headers=['content-type'])
def hello():
    return 'root'


@app.route('/user', methods=ALL_METHODS)
@app.route('/users', methods=['GET', 'OPTIONS'])  # to get all users. Same as GET /user
@app.route('/user/<userId>', methods=['GET', 'PUT', 'POST' , 'DELETE' , 'OPTIONS'])  # TODO: remove PUT
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], headers=['content-type'])
def user(userId=None):
    return users.user_main(userId)


@app.route('/course', methods=ALL_METHODS)
@app.route('/courses', methods=['GET'])  # to get all courses. Same as GET /course
@app.route('/course/<courseId>', methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS'])  # TODO: remove PUT
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], headers=['content-type'])
def course(courseId=None):
    return courses.course_main(courseId)


@app.route('/offering', methods=ALL_METHODS)  # all offerings
@app.route('/offerings', methods=[GET])  # same as above
@app.route('/offering/<quarterId>', methods=['GET'])  # all offerings for a quarter
@app.route('/offerings/<quarterId>', methods=['GET'])  # same as above
@app.route('/offering/<quarterId>/<courseId>', methods=[GET, DELETE])  # all offerings for a course in a quarter
@app.route('/offerings/<quarterId>/<courseId>', methods=[GET, DELETE])  # same as above
@app.route('/offering/<quarterId>/<courseId>/<sectionId>', methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS'])  # specific offering
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], headers=['content-type'])
def offering(quarterId=None, courseId=None, sectionId=None):
    return offerings.offering_main(quarterId, courseId, sectionId)


@app.route('/professor/<professorId>', methods=['GET', 'PUT' , 'POST' , 'DELETE' , 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], headers=['content-type'])
def professor(professorId=None):
    professors.professor_main(professorId)


@app.route('/quarter/<quarterId>', methods=['GET', 'PUT' , 'POST' , 'DELETE' , 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], headers=['content-type'])
def quarter(quarterId=None):
    return quarters.quarter_main(quarterId)


@app.route('/recommend/<userId>', methods=['GET'])
def getRecommendations(userId):
    pass


@app.route('/register', methods=['PUT', 'POST', 'DELETE', 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], headers=['content-type'])
def registerForCourse():
    return registration.register_main()

@app.route('/lookup/<studentId>/<quarterId>', methods=['GET'])
@crossdomain(origin='*', methods=['GET', 'OPTIONS'], headers=['content-type'])
def scheduleLookup(studentId, quarterId):
    return registration.registerGet(studentId, quarterId)


@app.route('/generateSchedules/', methods=['POST'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
def generateSchedules():
    pass


if __name__ == '__main__':
    print("You are running flaskServer.py directly; it will probably fail")
    app.run(host='0.0.0.0', port=5005)
