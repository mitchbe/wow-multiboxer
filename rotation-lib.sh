#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters - Window ID required"
    exit 1
fi

WIN_ID=$1
echo "Sending key events to window: $WIN_ID"

function keyboard_press () {
	keys=$1
	xdotool key --clearmodifiers --window $WIN_ID --delay 27 $keys
	echo $1
}

function rand() {
	min=$1
	max=$2
	local res=$(( $RANDOM % $max + $min ))
	echo "$res"
}

#foo=$(rand 2 200)
#echo foo is $foo
