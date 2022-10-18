#!/bin/bash
source rotation-lib.sh

keyboard_press "s F2 f"
keyboard_press "1"
sleep 1.$(rand 55 99)
while true 
do
	keyboard_press "2"
	sleep 1.$(rand 55 99)
done
