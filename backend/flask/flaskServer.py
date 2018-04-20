from flask import Flask, request, Response, json, Blueprint, send_from_directory
from crossorigin import crossdomain

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
def user(userId):
    if request.method == 'GET':
        return userGet(request)
    if request.method == 'PUT':
        return userPut(request)
    if request.method == 'POST':
        return userPost(request)
    if request.method == 'DELETE':
        return userDelete(request)

def userGet(request):
    content = request.get_json()
    pass

def userPut(request):
    pass

def userPost(request):
    pass

def userDelete(request):
    pass

@app.route('/course/<courseId>', methods=['GET'])
@app.route('/course/<courseId>', methods=['PUT'])
@app.route('/course/<courseId>', methods=['POST'])
@app.route('/course/<courseId>', methods=['DELETE'])
@app.route('/course/<courseId>', methods=['OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
def course(courseId):
    if request.method == 'GET':
        return courseGet(request)
    if request.method == 'PUT':
        return coursePut(courseId, request)
    if request.method == 'POST':
        return coursePost(request)
    if request.method == 'DELETE':
        return courseDelete(request)

@app.route('/offering/<offeringId>', methods=['GET'])
@app.route('/offering/<offeringId>', methods=['PUT'])
@app.route('/offering/<offeringId>', methods=['POST'])
@app.route('/offering/<offeringId>', methods=['DELETE'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
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
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
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
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
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

def coursePut(courseId, request):
    return Response(response=json.dumps(request.get_json()), status=200, mimetype='application/json')



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
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
def registerForCourse(userId, offeringId):
    pass

@app.route('/generateSchedules/', methods=['POST'])
@crossdomain(origin='*', methods=['GET', 'POST', 'PUT', 'DELETE'], headers=['content-type'])
def generateSchedules():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
