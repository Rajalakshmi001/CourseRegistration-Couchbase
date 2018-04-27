import requests
import json
from requests import Response
url = "http://137.112.89.91:5005" if 1 else "http://localhost:5005" 
uri = lambda x: url+x


def delete(path):
    print("--------------- DELETE")
    r = requests.delete(path)
    print(r.status_code, r.text)
    return r.status_code


def put(path, data):
    print("---------------- PUT")
    r = requests.put(path, json=data)  # type: Response
    print(r.status_code, r.text)
    return r.status_code


def get(path):
    print("---------------- GET")
    r = requests.get(path)  # type: Response
    print(r.content)
    returned = r.json() if r.content else None
    print(r.status_code, "GET returned:", returned)
    return returned


def get_all(path):
    print("---------------- GET ALL")
    r = requests.get(path)  # type: Response
    returned = r.json() if r.content else None
    print("> GET ALL returned:", returned)
    return returned


def post(path, data):
    print("---------------- POST")
    r = requests.post(path, data)
    return r.status_code


def test_all(sample_data: dict, sample_path: str, all_path=None, others_for_all=None, post_changes=None):
    sample_path = uri(sample_path)
    # delete
    delete(sample_path)
    # get should return null
    assert not get(sample_path)
    # put
    assert 200 <= put(sample_path, sample_data) < 304
    # get should return data
    assert get(sample_path) == sample_data

    if all_path:
        all_path = uri(all_path)
        if others_for_all:
            for other_path, other_data in others_for_all:
                assert 200 <= put(uri(other_path), other_data) <= 304
        else:
            others_for_all = []
        # get all should contain sample
        all_res = get_all(all_path)
        assert sample_data in all_res
        for _,other in others_for_all:
            assert other in all_res
    else:
        print("Not testing 'get all' functionality because path was not given")
    
    if post_changes:
        updated = {k:v for k,v in list(sample_data)}
        for k in post_changes:
            updated[k] = post_changes[k]
        post(sample_path, updated)

        assert get(sample_path) == updated
    else:
        print("not testing post")

    # delete again
    delete(sample_path)
    # and check for None again
    assert not get(sample_path)
