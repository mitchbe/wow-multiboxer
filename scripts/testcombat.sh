#!/bin/bash


WIN_ID=$(xwininfo -name "World of Warcraft" | grep "Window id" | cut -d ' ' -f 4 )
rm out/*
xwd -id $WIN_ID | convert xwd:- out/bigsnap.bmp
convert out/bigsnap.bmp -crop '15x30+15+73' out/snap.bmp
#convert out/snap.bmp -channel R -separate out/snapr.png
convert out/snap.bmp -map pallette.png out/snaprp.png 
convert histogram:out/snaprp.png -format %c histogram:info:- | grep red | wc -l

#echo "identify -precision 5 -define identify:locate=maximum -define identify:limit=3 out/tmpx.png" 

#DO_WIN_ID=$(xdotool search --name "World of Warcraft")
#echo "win id: $DO_WIN_ID"


#echo "convert out/snap.bmp -crop '15x30+15+73' out/a.png"

#convert histogram:red-combat.png -format %c histogram:info:-
