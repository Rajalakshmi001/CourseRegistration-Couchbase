from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.exceptions import NotFoundError
from couchbase.result import OperationResult, ValueResult
cluster = Cluster('couchbase://137.112.89.94:8091')
__authenticator = PasswordAuthenticator('admin2', 'An3WeeWa')
cluster.authenticate(__authenticator)
# cb = cluster.open_bucket('beer-sample')
# print(cb.get('21st_amendment_brewery_cafe'))
# manager = cluster.cluster_manager()  # didn't work; needed to use Admin
# manager.bucket_create('courses') 