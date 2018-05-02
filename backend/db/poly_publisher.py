
# kafka details

class Publisher(object):
    
    @property
    def topic(self):
        raise NotImplementedError("Did not set topic for", type(self))

    def send(self, topic, command, category, data):
        print("Send to kafka-{}:".format(topic), dict(command=command, category=category, data=data))
        print()
        return False

    def create(self, category, data=None, **kwargs):
        self.send(self.topic, "CREATE", category, (data or kwargs))


class RedisPublisher(Publisher):
    __instance = None
    def __new__(cls):
        if RedisPublisher.__instance is None:
            RedisPublisher.__instance = object.__new__(cls)
        return RedisPublisher.__instance   

    @property
    def topic(self):
        return "REDIS" 

    def create_course(self, course_data):
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

n4jp = Neo4JPublisher()
n4jp.save_enrollment("test_user", "test_course")