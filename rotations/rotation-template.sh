#!/bin/bash
source rotation-lib.sh

while true 
do
	keyboard_press "F2 1"
	sleep 1.$(rand 80 99)
	keyboard_press "F2 8"
	sleep 1.$(rand 50 70)
	sleep 1.5
	keyboard_press "f 2"
	sleep 1.$(rand 50 70)
	keyboard_press "Shift_L+1"
	sleep 9.$(rand 0 20)
	keyboard_press "Shift_L+="
	sleep 2.$(rand 0 10)
done
