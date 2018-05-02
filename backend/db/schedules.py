from itertools import chain
from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
import couchbase.subdocument as subdoc 
from adb_utils import catch_missing, require_json_data, catch_already_exists, json_response, SubdocPathNotFoundError
from db.offerings import offeringGet
import db.registration as registration


sched_bucket = cluster.open_bucket('schedules')


@catch_missing
def get_user_schedule(studentId, quarterId):
    return json_response(sched_bucket.get(studentId+'-'+quarterId).value)


def all_schedules_for(username):
    return list(sched_bucket.n1ql_query('SELECT quarterId,offerings,studentId FROM schedules WHERE studentId="{}"'.format(username)))


def all_enrollments_for_user(username, schedules=None):
    if not schedules:
        schedules = all_schedules_for(username)
    return pull_enrollments(schedules)


def pull_enrollments(schedules):
    return list(chain(*(((qid,) + item for item in offerings.items()) for qid,offerings in [(sched['quarterId'], sched['offerings']) for sched in schedules] if len(offerings))))  # Python is ridiculous and I love it


def del_all_scheds_for(username):
    # from db.registration import unregister  # TODO: guessing there would be an import circle otherwise. Should refactor to get rid of that.
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
