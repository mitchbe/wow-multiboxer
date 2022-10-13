#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters - Window ID required"
fi

WIN_ID=$1
echo $WIN_ID

function keyboard_press () {
	keys=$1
	xdotool key --clearmodifiers --window $WIN_ID --delay 27 $keys
	echo $1
}


while true 
do
	keyboard_press "F2 1"
	sleep 1.8
	keyboard_press "F2 8"
	sleep 1.5
	keyboard_press "f 2"
	sleep 1.5
	keyboard_press "Shift_L+1"
	sleep 9
	keyboard_press "Shift_L+="
	sleep 2
done
