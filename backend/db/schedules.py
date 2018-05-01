from flask import Flask, request, Response, json, make_response
from db.couchbase_server import *
import couchbase.subdocument as subdoc 
from adb_utils import catch_missing, require_json_data, catch_already_exists, json_response, SubdocPathNotFoundError
from db.offerings import offeringGet


sched_bucket = cluster.open_bucket('schedules')


def get_user_schedule(studentId, quarterId):
    return json_response(sched_bucket.get(studentId+'-'+quarterId, quiet=True).value)
