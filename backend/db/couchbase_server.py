from couchbase.cluster import Cluster, PasswordAuthenticator
from couchbase.exceptions import NotFoundError, KeyExistsError
from couchbase.result import OperationResult, ValueResult
from couchbase.admin import Admin
import couchbase.subdocument as subdoc 

SERVER_IP = "137.112.89.94"

cluster = Cluster('couchbase://{}:8091'.format(SERVER_IP))
__authenticator = PasswordAuthenticator('admin2', 'An3WeeWa')
cluster.authenticate(__authenticator)

adm = Admin('admin', 'An3WeeWa', host=SERVER_IP, port=8091)


class Buckets():
    offering_bucket = cluster.open_bucket('offerings')
    schedule_bucket = cluster.open_bucket('schedules')
    user_bucket = cluster.open_bucket('users')
    course_bucket = cluster.open_bucket('courses')

    _all =  [offering_bucket, schedule_bucket, user_bucket, course_bucket]
    _timeout = 2.000

    for bucket in _all:
        bucket.timeout = _timeout


if __name__ == '__main__':
    bckt = input("Enter bucket name to create: ")
    if not bckt:
        exit(0)
    res = adm.bucket_create(bckt)
    print(res)


"""
CREATE INDEX `quarterId` ON `schedules`(`quarterId`)
CREATE INDEX `schedCourses` ON `schedules`(`offerings`)
CREATE INDEX `studentId` ON `schedules`(`studentId`)



"""
