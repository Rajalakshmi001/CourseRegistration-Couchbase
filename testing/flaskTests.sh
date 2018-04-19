curlOutput=$(curl -X GET 137.112.89.91:5005/ -s -w '%{http_code}')
echo -e ">> ${curlOutput}"
correct="hello"
if [ "$curlOutput" = "$correct" ] ; then
	echo -e "replaced get pass"
else
	echo -e "failed: should be $correct"
	exit 1
fi
