## Course Registration
This is a course registration application with couchbase as a primary database. This app supports features such as 
1. Adding course information
2. Search course
3. Recommend courses

To take advantage of the key strong points of different databases, three different databases are used.
1. Couchbase - Primary database for storage.
2. Redis     - Search (https://github.com/Rajalakshmi001/CourseRegistration-Redis)
3. Neo4J     - Recommendation (https://github.com/Rajalakshmi001/CourseRegistration-Neo4J)

In order to maintain the seamless functionality, Kafka is used to send messages to update the databases in case of failure.

## VM Information
Flask server - 21

CouchBase - 22, 23, 24  
Neo4j - 23  
redis - 22
