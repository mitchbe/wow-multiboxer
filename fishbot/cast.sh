#!/bin/bash


	#xwd -id $WIN_ID | convert out/baseline.bmp xwd:-  -composite -compose difference \
#	convert out/baseline.bmp out/snap.bmp -composite -compose difference \
#		\( -brightness-contrast 0,35 -gamma 10  \) \
#		\( -fill black -fuzz 50% +opaque "#ffffff" \) \
#		\( -colors 2 -colorspace gray  -normalize  \) out/$i.png
# ORIGINAL OPERATIONS 
#	xwd -id $WIN_ID | convert xwd:- out/snap.bmp
#	composite out/baseline.bmp out/snap.bmp -compose difference tmp.png 
#	convert tmp.png -brightness-contrast 0,35 -gamma 10 out/tmp2.png
#	convert out/tmp2.png -fill black -fuzz 50% +opaque "#ffffff" out/tmp.png
#	convert out/tmp.png -colors 2 -colorspace gray  -normalize  out/$i.png
#	score=$(convert histogram:out/$i.png -format %c histogram:info:-  | tail -n 1 | awk '{print $1}'| sed 's:.$::')
function get_score() {
	#t1=$(date +%s%3N); 
#	score = $(xwd -id $WIN_ID | \
	xwd -id $WIN_ID | \
	composite out/baseline.bmp xwd:- -compose difference miff:- | \
		#\( -fill black -stroke black -draw "rectangle 327,800 727,900" \) \ # Hide cast bar when interface is open
	convert miff:- -brightness-contrast 0,35 -gamma 10  \
		\( -fill black -fuzz 50% +opaque "#ffffff" \) \
		\( -colors 2 -colorspace gray  -normalize  \) out/tmp.png  
	score=$(convert histogram:out/tmp.png -format %c histogram:info:-  | tail -n 1 | awk '{print $1}'| sed 's:.$::')
	#t2=$(date +%s%3N); 
	#echo "$((t2-t1)) ms"
	echo "$score"

	#\( -colors 2 -colorspace gray  -normalize  \) miff:- | \
	#tail -n 1 | awk '{print $1}'| sed 's:.$::') 
}

function get_coords() {
	xwd -id $WIN_ID | \
	composite out/baseline.bmp xwd:- -compose difference miff:- | \
	#	\( -fill black -stroke black -draw "rectangle 327,800 727,900" \) \ # Hide cast bar for when interface is open
	convert miff:- -brightness-contrast 0,35 -gamma 10  \
		\( -fill black -fuzz 50% +opaque "#ffffff" \) \
		\( -colors 2 -colorspace gray  -normalize  \) out/tmpx.png  
	#convert out/tmpx.png -fill black -stroke black -draw "rectangle 327,800 727,900" out/tmpy.png
	local coords=$(identify -precision 5 -define identify:locate=maximum -define identify:limit=3 out/tmpx.png | tail -n 1 | awk '{print $4}')
	x=$(echo $coords | cut -d ',' -f 1)
	y=$(echo $coords | cut -d ',' -f 2)
}

function catch_fish() {
	sleep 0.2
	xdotool mousemove --window $DO_WIN_ID --sync --clearmodifiers $x $y
	xdotool keydown --window $DO_WIN_ID Shift_L
	sleep 0.3
	xdotool mousedown --window $DO_WIN_ID 3
	sleep 0.1
	xdotool mouseup --window $DO_WIN_ID 3
#	xdotool keyup --window $DO_WIN_ID Shift_L
	xdotool key --window $DO_WIN_ID Shift_L
#	xdotool keyup Shift_L
	sleep 0.2
	xdotool mousemove --clearmodifiers 999999 999999
	echo "catch"
}

WIN_ID=$(xwininfo -name "World of Warcraft" | grep "Window id" | cut -d ' ' -f 4 )
echo $WIN_ID
echo "xwd -id $WIN_ID | convert xwd:- out/baseline.bmp"
rm out/*
xwd -id $WIN_ID | convert xwd:- out/baseline.bmp


DO_WIN_ID=$(xdotool search --name "World of Warcraft")
echo "win id: $DO_WIN_ID"

#xdotool mousemove --window $DO_WIN_ID --sync --clearmodifiers 200 100 
#exit 1

xdotool key --window $DO_WIN_ID --clearmodifiers 1
sleep 4
started=0
for i in {1..50}
do
	score=$(get_score)
	#score=$((score))
	echo "score:  $score"
	if [ $started -eq 0 ]; then
		#if [[ $(($score)) -le 28 ||  $(($score)) -ge 99999 ]]; then 
		if [[ $(($score)) -ge 99999 ]]; then 
			sleep 2
			continue
		else 
			started=1
			threshold=$(($score+($score/2)))
			get_coords
			echo "thres: $threshold; float-x: $x, float-y:$y"
		fi
	else	
		if [[ $(($score)) -le 5 || $(($score)) -ge 99999 ]]; then 
			echo "FINISHED"
			break
		fi
	fi

	if [ $((score)) -ge $((threshold)) ]; then
		echo "CATCH"
		catch_fish
		break;
	fi

done

