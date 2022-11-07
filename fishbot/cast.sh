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


function get_local_score() {
	#\( -fill black -stroke black -draw "rectangle 327,800 727,900" \) \ # Hide cast bar when interface is open
	
	#echo "**** X,Y: $x, $y"
	#x=$1
	#y=$2
	#echo "**** X,Y: $x, $y"
	crop_x=$(echo "$x-125" | bc)
	crop_y=$(echo "$y-125" | bc)
	crop_float="250x250+$crop_x+$crop_y"
	#echo "cropping: $crop_float"
	#convert miff:- -fill black -stroke black -draw "rectangle 0,800 1000,1100" miff:- | \
		
	xwd -id $WIN_ID | \
	composite out/baseline.bmp xwd:- -compose difference miff:- | \
	convert miff:$img -crop "$crop_float" miff:- | \
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

function get_score() {
	#\( -fill black -stroke black -draw "rectangle 327,800 727,900" \) \ # Hide cast bar when interface is open
	
		
	xwd -id $WIN_ID | \
	composite out/baseline.bmp xwd:- -compose difference miff:- | \
	convert miff:- -fill black -stroke black -draw "rectangle 0,800 1000,1100" miff:- | \
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
	#	\( -fill black -stroke black -draw "rectangle 327,800 727,900" \) \ # Hide cast bar for when interface is open
	xwd -id $WIN_ID | \
	composite out/baseline.bmp xwd:- -compose difference miff:- | \
	convert miff:- -fill black -stroke black -draw "rectangle 0,800 1000,1100" miff:- | \
	convert miff:- -brightness-contrast 0,35 -gamma 10  \
		\( -fill black -fuzz 50% +opaque "#ffffff" \) \
		\( -colors 2 -colorspace gray  -normalize  \) out/tmpx.png  
	#convert out/tmpx.png -fill black -stroke black -draw "rectangle 327,800 727,900" out/tmpy.png
	local coords=$(identify -precision 5 -define identify:locate=maximum -define identify:limit=3 out/tmpx.png | tail -n 1 | awk '{print $4}')
	x=$(echo $coords | cut -d ',' -f 1)
	y=$(echo $coords | cut -d ',' -f 2)
}


function get_baseline() {
	#echo "xwd -id $WIN_ID | convert xwd:- out/baseline.bmp"
	#xwd -id $WIN_ID | convert xwd:- out/baseline.bmp
	#echo "xwd -id $WIN_ID | convert xwd:- out/baseline.bmp"
	for i in {1..4}
	do
		echo "xwd -id $WIN_ID | convert xwd:- out/base$i.bmp"
		xwd -id $WIN_ID | convert xwd:- out/base$i.bmp
		sleep 0.3
	done
	convert out/base1.bmp out/base2.bmp out/base3.bmp out/base4.bmp -evaluate-sequence Mean out/baseline.bmp
}

function catch_fish() {
	echo "Catching..."
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
	echo "Caught!"
}

WIN_ID=$(xwininfo -name "World of Warcraft" | grep "Window id" | cut -d ' ' -f 4 )
echo $WIN_ID

#WIN_ID=$1
#echo $WIN_ID
rm out/*

## Take Baseline image
get_baseline


DO_WIN_ID=$(xdotool search --name "World of Warcraft")
echo "win id: $DO_WIN_ID"
#xdotool mousemove --window $DO_WIN_ID --sync --clearmodifiers 200 100 
#exit 1

## Cast: Fishing
echo "Cast: Fishing"
echo " -->  xdotool key --window $DO_WIN_ID --clearmodifiers 1"
xdotool key --window $DO_WIN_ID --clearmodifiers 1
sleep 4
started=0
for i in {1..150}
do
	if [ $started -eq 0 ]; then
		score=$(get_score)
	else 
		score=$(get_local_score $x $y)
	fi

	echo "Variation Score:  $score"
	if [ $started -eq 0 ]; then
		#if [[ $(($score)) -le 28 ||  $(($score)) -ge 99999 ]]; then 
		if [[ $(($score)) -ge 99999 ]]; then 
			sleep 2
			continue
		else 
			started=1
			threshold=$(bc <<< "$score+($score*0.4)")
			threshold=$(printf "%.0f" "$threshold")
			get_coords
			echo "Float appeared! x,y: $x,$y; variation trigger: $threshold"
		fi
	else	
		if [[ $(($score)) -le 5 || $(($score)) -ge 99999 ]]; then 
			echo "Float vanished!"
			break
		fi
	fi

	if [ $((score)) -ge $((threshold)) ]; then
		echo "Variation triggered..."
		catch_fish
		break;
	fi

done

