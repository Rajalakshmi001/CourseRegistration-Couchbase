from neo4j.v1 import GraphDatabase, basic_auth
from neo4j.v1.direct import DirectDriver, BoltSession
from adb_utils import json_response


__driver = GraphDatabase.driver("bolt://433-24.csse.rose-hulman.edu",auth=basic_auth("neo4j","An3WeeWa"))  # type: DirectDriver


def run_cmd(cmd):
    # print("> $ ", cmd)
    session = __driver.session()
    return list(session.run(cmd))


def match(cmd):
    fetched = run_cmd(cmd)
    return list(node[0].properties for node in fetched)


def recommend_courses_for(userId):
    query_str = "MATCH (s1:Student {studentId: '"+userId+"'})-[r:Enrolled]->(c1:Course)<-[r2:Enrolled]-(s2:Student)-[r3:Enrolled]->(c3:Course) RETURN c3"
    matches =  match(query_str)

    coursenums = set(entry['courseNum'] for entry in matches if 'courseNum' in entry)

    return list(dict(courseNum=cn) for cn in coursenums)


def recommend_main(userId):
    return json_response(recommend_courses_for(userId))


print(recommend_courses_for("reg_test_user_1"))