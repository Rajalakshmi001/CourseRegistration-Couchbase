from test_methods import test_all, delete, uri


def test_users():
    print(">>> Testing users")
    test_user_path = '/user/my_test_user'
    all_user_path = '/user'
    test_user_data = dict(
            username='my_test_user', 
            name='test user')

    test_all(test_user_data, test_user_path, all_user_path)
    print("\n>> Done testing users\n\n")


def test_courses():
    print(">>> Testing courses")
    test_course_path = '/course/TEST123'
    all_courses_path = '/course'
    test_course_data = dict(courseNum='TEST123', sectionNum="01", description='this is a test course', name='Test Course')
    test_all(test_course_data, test_course_path, all_courses_path)
    print("\n>> Done testing courses\n\n")


def test_offerings():
    print(">>> Testing offerings")
    delete(uri('/quarter/Summer2000'))
    test_offering_data = dict(professor="TEST_PROF", sectionId="01", courseId="OTestCourse", quarterId="Summer2000")
    test_offering_path = "/offering/Summer2000/OTestCourse/01"
    others = [["/offering/Summer2000/OTestCourse/02", 
                dict(professor="SECOND_TEST_PROF", sectionId="02", courseId="OTestCourse", quarterId="Summer2000")]]
    test_all(test_offering_data, test_offering_path, "/offering/Summer2000/OTestCourse", others)
    delete(uri('/quarter/Summer2000'))


test_users()
test_courses()
test_offerings()