import requests, json, os
from requests import Response
from time import sleep
from functools import partial, wraps


print = partial(print, flush=True)

DO_LOCAL = not os.getenv("CI")
url = "http://localhost:5005"  if DO_LOCAL else "http://137.112.89.91:5005" 
uri = lambda x: url+x

print("DOING {} TESTS".format("LOCAL" if DO_LOCAL else "REMOTE"))

def retry_504(function):
    @wraps(function)
    def wrapper(*a, **kwa):
        ret = function(*a, **kwa)
        try:
            if isinstance(ret, int):
                assert ret != 504
            elif isinstance(ret, list) or isinstance(ret, tuple):
                assert ret[-1] != 504
            return ret
        except AssertionError:
            print("Retrying due to 504", ">" * 50,'')
            return function(*a, **kwa)
    return wrapper

try:
    requests.get(url)
    print("Connected")
except:
    print("Could not connect")
    exit(1)


@retry_504
def delete(path, data=None):
    print("--------------- DELETE", path)
    r = requests.delete(path, data)
    print(r.status_code, r.text)
    return r.status_code


@retry_504
def put(path, data):
    print("---------------- PUT", path)
    print("\t", data)
    r = requests.put(path, json=data)  # type: Response
    print(r.status_code, r.text)
    sleep(1)
    return r.status_code


@retry_504
def get(path, include_code=False):
    print("---------------- GET", path)
    r = requests.get(path)  # type: Response
    try:
        returned = r.json() if r.content else None
    except:
        raise Exception("JSON decode failed", r.content)
    print(r.status_code, "GET returned:", returned)
    if include_code:
        return [returned, r.status_code]
    return returned


@retry_504
def get_all(path):
    print("---------------- GET ALL", path)
    r = requests.get(path)  # type: Response
    returned = r.json() if r.content else None
    print("> GET ALL returned:", returned)
    return returned


@retry_504
def post(path, data):
    print("---------------- POST", path)
    r = requests.post(path, data)
    return r.status_code


def test_all(sample_data: dict, sample_path: str, all_path=None, others_for_all=None, post_changes=None):
    sample_path = uri(sample_path)
    others_for_all = others_for_all or []
    # delete
    delete(sample_path)
    # get should return null
    assert not get(sample_path)
    # put gives 200-level code
    assert 200 <= put(sample_path, sample_data) < 300
    # put again returns 304
    assert 304 == put(sample_path, sample_data)
    # get should return data
    assert get(sample_path) == sample_data

    if all_path:
        all_path = uri(all_path)
        for other_path, other_data in others_for_all:
            assert 200 <= put(uri(other_path), other_data) <= 304
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
        print("\nnot testing POST\n")

    # delete again
    delete(sample_path)
    # and check for None again
    assert not get(sample_path)
