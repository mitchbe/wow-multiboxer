#!/bin/bash
source rotation-lib.sh

keyboard_press "s f2 f"
while true 
do
	keyboard_press "1"
	sleep 1.$(rand 55 99)
done
