#!/bin/bash
curlOutput=$(curl -X GET 137.112.89.91:5005 -s)
echo -e ">> ${curlOutput}"
correct="hello"
if [ "$curlOutput" = "$correct" ] ; then
	echo -e "top-level get passed"
else
	echo -e "top-level get failed; should be $correct"
	exit 1
fi