from time import sleep
from test_methods import *


user1 = dict(username='reg_test_user_1', name='registration test user 1')
user2 = dict(username='reg_test_user_2', name='registration test user 2')
user3 = dict(username='reg_test_user_3', name='registration test user 3')

t_o = test_offering = dict(quarter='rquarter1', courseNum='RegTestCourse', offeringId='01', capacity=2)
quarter = t_o['quarter']

reg_uri = uri('/register')

def del_user(user):
    delete(uri('/user/'+user['username']))

def reg_tests():
    print("\n\n>>> Doing registration tests\n")

    # delete, add offering
    off_uri = uri('/'.join(('/offering', quarter, t_o['courseNum'], t_o['offeringId'])))
    delete(off_uri) #(uri('/offering/' + quarter +'/'+test_offering['courseNum']))
    assert 201 == put(uri('/offering'), test_offering)
    get(off_uri)
    print("Go look at offerings")
    # sleep(10)
    # delete, add users
    for user in [user1, user2, user3]:
        delete(uri('/user/'+user['username']))
        put(uri('/user'), user)

    # register user1, user2
    reg_request = lambda user: dict(studentId=user['username'], quarterId=t_o['quarter'], 
                        courseNum=t_o['courseNum'], offeringId=t_o['offeringId'])
    for i,user in enumerate([user1, user2]):
        rr = reg_request(user)
        assert(put(reg_uri, rr) == 201)
        get(off_uri)
        assert(put(reg_uri, rr) >= 300)
        print("Check offering, just registered user")
        go = get(off_uri)
        # sleep(10)
        assert go['enrolled'] == i+1

    assert put(reg_uri, reg_request(user3)) >= 400
    assert get(off_uri)['enrolled'] == 2
    
    print("\n>> Done testing courses\n\n")


if __name__ == '__main__':
    reg_tests()