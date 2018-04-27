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


def __set_up_couchbase():
    if input("Enter 'confirm' to confirm couchbase setup: ") != 'confirm':
        return

    # for bucket in ['users', 'courses', 'schedules']
    adm.bucket_create('users')


if __name__ == '__main__':
    bckt = input("Enter bucket name to create: ")
    if not bckt:
        exit(0)
    res = adm.bucket_create(bckt)
    print(res)


"""
n1ql:> CREATE PRIMARY INDEX username ON users
CREATE PRIMARY INDEX courseNum ON courses
CREATE PRIMARY INDEX 

"""