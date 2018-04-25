from flask import Flask, request, Response, json, Blueprint, send_from_directory
from flask_server.crossorigin import crossdomain
from db import courses,users,offerings,quarters,professors,registration


app = Flask(__name__)


@app.route('/')
@crossdomain(origin='*', methods=['GET'], headers=['content-type'])
def hello():
    return 'root'

@app.route('/user', methods=['GET'])
@app.route('/user/<userId>', methods=['GET'])
@app.route('/user/<userId>', methods=['PUT'])
@app.route('/user/<userId>', methods=['POST'])
@app.route('/user/<userId>', methods=['DELETE'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
def user(userId=None):
    return users.user_main(userId)


@app.route('/course/<courseId>', methods=['GET'])
@app.route('/course/<courseId>', methods=['PUT'])
@app.route('/course/<courseId>', methods=['POST'])
@app.route('/course/<courseId>', methods=['DELETE'])
@app.route('/course/<courseId>', methods=['OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], headers=['content-type'])
def course(courseId=None):
    return courses.course_main(courseId)


@app.route('/offering/<quarterId>/<courseId>/<sectionId>', methods=['GET'])
@app.route('/offering/<quarterId>/<courseId>/<sectionId>', methods=['PUT'])
@app.route('/offering/<quarterId>/<courseId>/<sectionId>', methods=['POST'])
@app.route('/offering/<quarterId>/<courseId>/<sectionId>', methods=['DELETE'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
def offering(quarterId=None, courseId=None, sectionId=None):
    return offerings.offering_main(quarterId, courseId, sectionId)


@app.route('/professor/<professorId>', methods=['GET'])
@app.route('/professor/<professorId>', methods=['PUT'])
@app.route('/professor/<professorId>', methods=['POST'])
@app.route('/professor/<professorId>', methods=['DELETE'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
def professor(professorId=None):
    professors.professor_main(professorId)


@app.route('/quarter/<quarterId>', methods=['GET'])
@app.route('/quarter/<quarterId>', methods=['PUT'])
@app.route('/quarter/<quarterId>', methods=['POST'])
@app.route('/quarter/<quarterId>', methods=['DELETE'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
def quarter(quarterId=None):
    return quarters.quarter_main(quarterId)


@app.route('/recommend/<userId>', methods=['GET'])
def getRecommendations(userId):
    pass

@app.route('/register/<userId>/<offeringId>', methods=['GET'])
@app.route('/register/<userId>/<offeringId>', methods=['PUT'])
@app.route('/register/<userId>/<offeringId>', methods=['POST'])
@app.route('/register/<userId>/<offeringId>', methods=['DELETE'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
def registerForCourse(userId, offeringId):
    return registration.register_main(userId, offeringId)


@app.route('/generateSchedules/', methods=['POST'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
def generateSchedules():
    pass


if __name__ == '__main__':
    print("You are running flaskServer.py directly; it will probably fail")
    app.run(host='0.0.0.0', port=5005)
