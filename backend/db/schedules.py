from itertools import chain
from flask import Flask, request, Response, json, make_response
import db.couchbase_server as cb
from couchbase.exceptions import TimeoutError
import couchbase.subdocument as subdoc 
from adb_utils import catch_missing, require_json_data, catch_already_exists, json_response, SubdocPathNotFoundError
import db.registration as registration


sched_bucket = cb.Buckets.schedule_bucket


def get_user_schedule(studentId, quarterId):
    # print("\n\nlookup")
    sbg = sched_bucket.get(studentId+'-'+quarterId, quiet=None)
    val = sbg.value
    # try:
    # except TimeoutError as te:
    #     print("Retrying with more time than", sched_bucket.timeout,"-- type(e) is", type(te), "class is", te.__class__)
    #     sbg = sched_bucket.get(studentId+'-'+quarterId)
    #     return json_response(sbg.value)
    # except Exception as e:
    #     print(">"*6, "was not TimeoutError; was", type(e))
    #     val = None
    return val  # json_response(val)


@catch_already_exists
def initialize_user_schedule(studentId, quarterId):
    sched_key = studentId+"-"+quarterId
    try:
        print("INSERTING SCHEDULE FOR", sched_key)
        return sched_bucket.insert(sched_key, {"studentId": studentId, "quarterId": quarterId})
    except:
        return False
        

def all_schedules_for(username):
    return list(sched_bucket.n1ql_query('SELECT quarterId,offerings,studentId FROM schedules WHERE studentId="{}"'.format(username)))


def all_enrollments_for_user(username, schedules=None):
    if not schedules:
        schedules = all_schedules_for(username)
    return pull_enrollments(schedules)


def pull_enrollments(schedules):
    return list(chain(*(((qid,) + item for item in offerings.items()) for qid,offerings in [(sched['quarterId'], sched['offerings']) for sched in schedules] if len(offerings))))  # Python is ridiculous and I love it


def del_all_scheds_for(username):
    print("Deleting all schedules for", username)
    # from db.registration import unregister
    schedules = all_schedules_for(username)
    # de-register from all classes
    enrollments = pull_enrollments(schedules)
    for enrollment in enrollments:
        try:
            registration.unregister(username, *enrollment)
        except:
            pass
    # delete all schedules
    quarters = list(entry['quarterId'] for entry in schedules)
    __unsafe_delete_user_schedules(username, *quarters)
    return True


def __unsafe_delete_user_schedules(username, *quarters):
    if not quarters or not len(quarters):
        return True
    sched_keys = list(username+'-'+quarter for quarter in quarters)
    sched_bucket.remove_multi(sched_keys, quiet=True)
    return True


def remove_course_from_sched(studentId, quarterId, courseNum, offeringId):
    """
    NOT count-safe
    """
    return sched_bucket.mutate_in(sched_key(studentId, quarterId), subdoc.remove(course_subkey(courseNum)))


def add_course_to_sched(studentId, quarterId, courseNum, offeringId):
    return sched_bucket.mutate_in(sched_key(studentId, quarterId), subdoc.insert(course_subkey(courseNum), offeringId, create_parents=True))


def sched_key(studentId, quarterId):
    return "{}-{}".format(studentId, quarterId)

def course_subkey(courseNum):
    return 'offerings.{}'.format(courseNum)
