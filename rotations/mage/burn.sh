#!/bin/bash
source rotation-lib.sh

keyboard_press "s F2 f"
keyboard_press "1"
sleep 2.$(rand 5 25)
keyboard_press "3"
sleep 1
while true 
do
	keyboard_press "2"
	sleep 1.$(rand 5 25)
done
