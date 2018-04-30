template = """
TEST_NAME="{}"
curlOutput=$(curl -X {} 137.112.89.91:5005{} -s --connect-timeout 5)
echo -e ">> ${{curlOutput}}"
correct="{}"
if [ "$curlOutput" = "$correct" ] ; then
	echo -e "${{GREEN}}${{TEST_NAME}} passed ${{NC}}"
else
	echo -e "${{RED}}${{TEST_NAME}} failed; should be ${{NC}} $correct"
	failedTests=1
fi
"""
test_name = input("Input test name (blank = method and path): ")
method = input("Input method (blank = GET): ") or 'GET'
path = input("Input path (blank=/): ") or '/'
expected = input("Input expected result: ")
if not test_name:
    test_name = method + " " + path

print(template.format(test_name, method, path, expected))