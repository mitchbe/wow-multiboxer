#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters - Window ID required"
fi

WIN_ID=$1
echo $WIN_ID

function keyboard_press () {
	keys=$1
	xdotool key --window $WIN_ID --delay 27 $keys
	echo $1
}


while true 
do
	keyboard_press "space"
	sleep 2
	keyboard_press "w w w w w w w w w w w w w w w w w w w w w w w w w"
	sleep 2
	keyboard_press "space"
	sleep 2
	keyboard_press "s s s s s s s s s s s s s s s s s s s s s s s s s"
	sleep 2
done
