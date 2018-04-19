from flask import Flask, request, Response, json, Blueprint, send_from_directory

app = Flask(__name__)


@app.route('/')
def hello():
    return 'root'

@app.route('/user', methods=['GET'])
@app.route('/user/<userId>', methods=['GET'])
@app.route('/user/<userId>', methods=['PUT'])
@app.route('/user/<userId>', methods=['POST'])
@app.route('/user/<userId>', methods=['DELETE'])
def user(userId):
    if request.method == 'GET':
        return userGet(request)
    if request.method == 'PUT':
        return userPut(request)
    if request.method == 'POST':
        return userPost(request)
    if request.method == 'DELETE':
        return userDelete(request)

def userGet():
    pass

def userPut():
    pass

def userPost():
    pass

def userDelete():
    pass

@app.route('/course/<courseId>', methods=['GET'])
@app.route('/course/<courseId>', methods=['PUT'])
@app.route('/course/<courseId>', methods=['POST'])
@app.route('/course/<courseId>', methods=['DELETE'])
def course():
    if request.method == 'GET':
        return courseGet(request)
    if request.method == 'PUT':
        return coursePut(request)
    if request.method == 'POST':
        return coursePost(request)
    if request.method == 'DELETE':
        return courseDelete(request)

@app.route('/offering/<offeringId>', methods=['GET'])
@app.route('/offering/<offeringId>', methods=['PUT'])
@app.route('/offering/<offeringId>', methods=['POST'])
@app.route('/offering/<offeringId>', methods=['DELETE'])
def offering(offeringId):
    if request.method == 'GET':
        return offeringGet(request)
    if request.method == 'PUT':
        return offeringPut(request)
    if request.method == 'POST':
        return offeringPost(request)
    if request.method == 'DELETE':
        return offeringDelete(request)

@app.route('/professor/<professorId>', methods=['GET'])
@app.route('/professor/<professorId>', methods=['PUT'])
@app.route('/professor/<professorId>', methods=['POST'])
@app.route('/professor/<professorId>', methods=['DELETE'])
def professor(professorId):
    if request.method == 'GET':
        return professorGet(request)
    if request.method == 'PUT':
        return professorPut(request)
    if request.method == 'POST':
        return professorPost(request)
    if request.method == 'DELETE':
        return professorDelete(request)

@app.route('/quarter/<quarterId>', methods=['GET'])
@app.route('/quarter/<quarterId>', methods=['PUT'])
@app.route('/quarter/<quarterId>', methods=['POST'])
@app.route('/quarter/<quarterId>', methods=['DELETE'])
def quarter(quarterId):
    if request.method == 'GET':
        return quarterGet(request)
    if request.method == 'PUT':
        return quarterPut(request)
    if request.method == 'POST':
        return quarterPost(request)
    if request.method == 'DELETE':
        return quarterDelete(request)

def courseGet():
    pass

def coursePut():
    pass

def coursePost():
    pass

def courseDelete():
    pass

@app.route('/recommend/<userId>', methods=['GET'])
def getRecommendations(userId):
    pass

@app.route('/register/<userId>/<offeringId>', methods=['GET'])
@app.route('/register/<userId>/<offeringId>', methods=['PUT'])
@app.route('/register/<userId>/<offeringId>', methods=['POST'])
@app.route('/register/<userId>/<offeringId>', methods=['DELETE'])
def registerForCourse(userId, offeringId):
    pass

@app.route('/generateSchedules/', methods=['POST'])
def generateSchedules():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)