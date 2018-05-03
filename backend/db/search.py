from random import randint
from flask import request
from redis import Redis

redis_client = Redis(
    host='localhost',
    port=6379,
    socket_timeout=2,
    socket_connect_timeout=2,
    retry_on_timeout=True,
    charset='utf-8',
    decode_responses=True)


def run_search(queryString=None, department=None):
    keywords = list(word.lower() for word in queryString.split(" ") if len(word) > 3)

    keyword_indices = sorted('ind:'+keyword for keyword in keywords)
    sus = "search_{}".format(randint(0,1000000))
    if department:
        redis_client.sunionstore(sus, keyword_indices)
        return redis_client.sinter(("dept:"+department, sus))

    return redis_client.sunion(keyword_indices)

    