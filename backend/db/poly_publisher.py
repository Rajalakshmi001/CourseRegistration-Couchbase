import json
from time import sleep
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='137.112.89.91:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# kafka details

class Publisher(object):
    """
    Make methods in the db publishers for each category-task pair. Should take in only the relevant data. 
    Example: create_course(self, course_data)
    In that method, call self.[task] with the category and data 
    Example: self.create("COURSE", course_data)
    """
    @property
    def topic(self):
        raise NotImplementedError("Did not set topic for", type(self))

    def send(self, command, category, data):
        msg = dict(command=command, category=category, data=data)
        print("Send to kafka topic <{}>:".format(self.topic), msg)
        producer.send(self.topic, msg)
        if __name__ == '__main__':
            sleep(1)
        return True

    def create(self, category, data=None, **kwargs):
        self.send("CREATE", category, (data or kwargs))

    def delete(self, category, data=None, **kwargs):
        self.send("DELETE", category, (data or kwargs))


class RedisPublisher(Publisher):
    __instance = None
    def __new__(cls):
        if RedisPublisher.__instance is None:
            RedisPublisher.__instance = object.__new__(cls)
        return RedisPublisher.__instance   

    @property
    def topic(self):
        return "redis" 

    def create_course(self, course_data):
        self.create("COURSE", course_data)

    def delete_course(self, course_data):
        self.delete("COURSE", course_data)

    def update_course(self, course_data):
        self.delete("COURSE", course_data)
        self.create("COURSE", course_data)

    
class Neo4JPublisher(Publisher):
    __instance = None
    def __new__(cls):
        if Neo4JPublisher.__instance is None:
            Neo4JPublisher.__instance = object.__new__(cls)
        return Neo4JPublisher.__instance   

    @property
    def topic(self):
        return "NEO4J"
    
    def save_enrollment(self, username, courseNum):
        self.create("enrollments", username=username, courseNum=courseNum)


rp = RedisPublisher()
rp.create_course(dict(courseNum="csse433", name="Advanced Databases"))

# n4jp = Neo4JPublisher()
# n4jp.save_enrollment("test_user", "test_course")
