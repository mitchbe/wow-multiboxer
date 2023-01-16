#!/bin/bash

while true
do
	echo "**CASTING**"
	./cast.sh
	sleep 5
	sleep .$[ ( $RANDOM % 3 ) + 1 ]s

done
