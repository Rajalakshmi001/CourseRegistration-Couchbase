#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'

failedTests=0


TEST_NAME="top-level get"
curlOutput=$(curl -X GET 137.112.89.91:5005 -s)
echo -e ">> ${curlOutput}"
correct="hello"
if [ "$curlOutput" = "$correct" ] ; then
	echo -e "${GREEN}${TEST_NAME} passed ${NC}"
else
	echo -e "${RED}${TEST_NAME} failed; should be ${NC} $correct"
	failedTests=1
fi


TEST_NAME="deliberately failing test"
curlOutput=$(curl -X GET 137.112.89.9:5005 -s --connect-timeout 5)
echo -e ">> ${curlOutput}"
correct="hello"
if [ "$curlOutput" = "$correct" ] ; then
	echo -e "${GREEN}${TEST_NAME} passed ${NC}"
else
	echo -e "${RED}${TEST_NAME} failed; should be ${NC} $correct"
	failedTests=1
fi


exit $failedTests
