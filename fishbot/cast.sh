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


function get_float_score() {
	crop_x=$(echo "$x-125" | bc)
	crop_y=$(echo "$y-125" | bc)
	crop_float="250x250+$crop_x+$crop_y"
	#echo "cropping: $crop_float"

		
	xwd -id $WIN_ID | \
	composite out/baseline.bmp xwd:- -compose difference miff:- | \
	convert miff:- -crop "$crop_float" miff:- | \
	convert miff:- -brightness-contrast 0,35 -gamma 10 miff:- | 
	convert miff:- -map ../pallettes/base_colour_pallette.png out/tmp.png
	#score=$(convert histogram:out/tmp.png -format %c histogram:info:-  | grep -v "#fffff" | awk '{print $1}'| sed 's:.$::')

	histogram=$(convert miff:$tmp -format %c histogram:info:-) 

	local white=$(($(echo -e "$histogram" | grep "FFFFFF" | awk '{print $1}'| sed 's:.$::')))
	local blue=$(($(echo -e "$histogram" | grep "0000FF" | awk '{print $1}'| sed 's:.$::')))
	if [[ $((white)) -gt $((blue)) ]]; then
		echo "1"
		return
	fi
	echo "0"

	#out/float_baseline.bmp00

	#\( -map pallettes/bnw_pallette.png out/diff-bnw.png \) out/float_baseline.png
	#\( -colors 2 -colorspace gray  -normalize  \) out/float_baseline.png  
	#echo "$score"
}


function get_local_score() {
	
	nr=$1

	crop_x=$(echo "$x-125" | bc)
	crop_y=$(echo "$y-125" | bc)
	crop_float="250x250+$crop_x+$crop_y"
	#echo "cropping: $crop_float"

	xwd -id $WIN_ID | \
	composite out/baseline.bmp xwd:- -compose difference miff:- | \
	convert miff:- -crop "$crop_float" miff:- | \
	convert miff:- -brightness-contrast 0,35 -gamma 10 "out/float$nr.bmp"
	score=$(convert histogram:out/tmp.png -format %c histogram:info:-  | grep -v "#fffff" | awk '{print $1}'| sed 's:.$::')

#		\( -fill black -fuzz 50% +opaque "#ffffff" \) \
		
	#convert xwd:- -crop "$crop_float" miff:- | \
#	composite out/float_baseline.bmp "out/float$nr.bmp" -compose difference miff:- | \
#	convert miff:- -blur 2x2 miff:- | \
#	convert miff:- -colors 2 -colorspace gray  -normalize  out/tmp.png  
        #convert miff:- -map pallettes/bnw_pallette.png out/tmp.png 


	#xwd -id $WIN_ID | \
	#convert xwd:- -crop "$crop_float" miff:- | \
	#composite out/float_baseline.bmp miff:- -compose difference miff:- | \
	#convert miff:- -colors 2 -colorspace gray  -normalize  out/tmp.png  
	score=$(convert histogram:out/tmp.png -format %c histogram:info:-  | grep -v "#000000" | awk '{print $1}'| sed 's:.$::')
	#echo "$score"
	echo "1"


#	xwd -id $WIN_ID | \
#	composite out/baseline.bmp xwd:- -compose difference miff:- | \
#	convert miff:$img -crop "$crop_float" miff:- | \
#	convert miff:- -brightness-contrast 0,35 -gamma 10  \
#		\( -colors 2 -colorspace gray  -normalize  \) out/tmp.png  
#	score=$(convert histogram:out/tmp.png -format %c histogram:info:-  | tail -n 1 | awk '{print $1}'| sed 's:.$::')
#	echo "$score"


	#\( -fill black -fuzz 50% +opaque "#ffffff" \) \
	#\( -colors 2 -colorspace gray  -normalize  \) miff:- | \
	#tail -n 1 | awk '{print $1}'| sed 's:.$::') 
}

function get_score() {
	#\( -fill black -stroke black -draw "rectangle 327,800 727,900" \) \ # Hide cast bar when interface is open
	
	## Debug	

	#xwd -id $WIN_ID | \
	#composite out/baseline.bmp xwd:- -compose difference miff:- | \
	#convert miff:- -fill black -stroke black -draw "rectangle 0,800 1000,1100" out/diff.png 
	#convert out/diff.png -brightness-contrast 0,35 -gamma 10  out/diff-bc.png 
	#convert out/diff-bc.png -colors 2 -colorspace gray  -normalize  out/diff-gray.png  
	##convert out/diff-gray.png -blur 3x3  out/diff-blur.png  
        ##convert out/diff-blur.png -map pallettes/bnw_pallette.png out/diff-bnw.png 
	##convert out/diff-bnw.png -fill black -fuzz 50% +opaque "#ffffff" out/diff-fuzz.png 
	#score=$(convert histogram:out/diff-gray.png -format %c histogram:info:-  | tail -n 1 | awk '{print $1}'| sed 's:.$::')

	#xwd -id $WIN_ID | \
	#composite out/baseline.bmp xwd:- -compose difference miff:- | \
	#convert miff:- -fill black -stroke black -draw "rectangle 0,800 1000,1100" miff:- | \
	#convert miff:- -brightness-contrast 0,35 -gamma 10  \
	#	\( -fill black -fuzz 50% +opaque "#ffffff" \) \
	#	\( -colors 2 -colorspace gray  -normalize  \) out/tmp.png  
	#score=$(convert histogram:out/tmp.png -format %c histogram:info:-  | tail -n 1 | awk '{print $1}'| sed 's:.$::')
	#echo "$score"



	xwd -id $WIN_ID | \
	composite out/baseline.bmp xwd:- -compose difference miff:- | \
	convert miff:- -fill black -stroke black -draw "rectangle 0,800 1000,1100" miff:- | \
	convert miff:- -brightness-contrast 0,35 -gamma 10  \
		\( -colors 2 -colorspace gray  -normalize  \) out/tmp.png  
	score=$(convert histogram:out/tmp.png -format %c histogram:info:-  | tail -n 1 | awk '{print $1}'| sed 's:.$::')
	echo "$score"

}

function get_coords() {
	#xwd -id $WIN_ID | \
	#composite out/baseline.bmp xwd:- -compose difference miff:- | \
	#convert miff:- -fill black -stroke black -draw "rectangle 0,800 1000,1100" miff:- | \
	#convert miff:- -brightness-contrast 0,35 -gamma 10  \
	#	\( -fill black -fuzz 50% +opaque "#ffffff" \) \
	#	\( -colors 2 -colorspace gray  -normalize  \) out/tmpx.png  


	xwd -id $WIN_ID | \
	composite out/baseline.bmp xwd:- -compose difference miff:- | \
	convert miff:- -fill black -stroke black -draw "rectangle 0,800 1000,1100" miff:- | \
	convert miff:- -brightness-contrast 0,35 -gamma 10  \
		\( -colors 2 -colorspace gray  -normalize  \) \
		\( -blur 3x3  \) out/tmpx.png

	local coords=$(identify -precision 5 -define identify:locate=maximum -define identify:limit=1 out/tmpx.png | tail -n 1 | awk '{print $4}')
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

function click_float() {
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

function float_hist() {
	#echo "Comparing float with float baseline.."
	#score=$(get_float_score $i)
	crop_x=$(echo "$x-75" | bc)
	crop_y=$(echo "$y-75" | bc)
	crop_float="150x150+$crop_x+$crop_y"
	#echo "cropping: $crop_float"
		

	xwd -id $WIN_ID | \
	composite out/baseline.bmp xwd:- -compose difference miff:- | \
	convert miff:- -crop "$crop_float" miff:- | \
	convert miff:- -brightness-contrast 0,35 -gamma 10 miff:- | \
	convert miff:- -map pallettes/base_colour_pallette.png out/tmp$i.png

	histogram=$(convert out/tmp$i.png -format %c histogram:info:-) 

	white=$(($(echo -e "$histogram" | grep "FFFFFF" | awk '{print $1}'| sed 's:.$::')))
	blue=$(($(echo -e "$histogram" | grep "0000FF" | awk '{print $1}'| sed 's:.$::')))
	red=$(($(echo -e "$histogram" | grep "FF0000" | awk '{print $1}'| sed 's:.$::')))
	green=$(($(echo -e "$histogram" | grep "00FF00" | awk '{print $1}'| sed 's:.$::')))
	yellow=$(($(echo -e "$histogram" | grep "FFFF00" | awk '{print $1}'| sed 's:.$::')))
	nr_colours=$(($(echo -e "$histogram" | wc -l )))
	colour_saturation=$((red+green+blue+yellow))

}

WIN_ID=$(xwininfo -name "World of Warcraft" | grep "Window id" | cut -d ' ' -f 4 )
echo $WIN_ID

#WIN_ID=$1
#echo $WIN_ID
rm out/*

## Take Baseline image
get_baseline


DO_WIN_ID=$(xdotool search --name "^World of Warcraft$")
echo "win id: $DO_WIN_ID"
#xdotool mousemove --window $DO_WIN_ID --sync --clearmodifiers 200 100 
#exit 1

## Cast: Fishing
echo "Cast: Fishing"
echo " -->  xdotool key --window $DO_WIN_ID --clearmodifiers 1"
xdotool key --window $DO_WIN_ID --clearmodifiers 1
sleep 4
started=0

for i in {1..20}
do
	score=$(get_score)
	score=$(($score))
	echo "Score:  $score"
	if [[ $score -ge 99999 ]]; then 
		sleep 2
	else 
		started=1
		get_coords
		echo "Float appeared! x,y: $x,$y;"
		float_hist
		echo "white/red/green/blue/yellow/nr_colours: $white,$red,$green,$blue,$yellow,$data"
		baseline_colour_saturation=$colour_saturation	
		baseline_white=$white

	#	echo "Capturing float baseline.."
	#	capture_float_baseline

		#local_score=$(get_local_score)
		#echo "Float baseline score: $local_score"
		#threshold=$(bc <<< "$local_score+($local_score*0.4)")
		#threshold=$(printf "%.0f" "$threshold")
		threshold=20
		#echo "Float appeared! x,y: $x,$y; Threshold score: $threshold"
		break
	fi
done



for i in {1..150}
do

	float_hist
	echo "-- white/red/green/blue/yellow/nr_colours: $white,$red,$green,$blue,$yellow,$data"
	
	#if [[ $((white)) -ne 0 ]]; then
	echo "White(white,baseline,diff): $white,$baseline_white,$((white-baseline_white))"
	#fi
	#if [[ $((colour_saturation)) -ne 0 ]]; then
	#	echo "White variation: $baseline_white / $white =  " $(echo "scale=2; $baseline_white / $white" | bc)
	colour_saturation_variation=$(echo "scale=2; $colour_saturation/$baseline_colour_saturation" | bc)
	#echo "Colour saturation variation: $baseline_colour_saturation/$colour_saturation=$colour_saturation_variation"
	echo "Saturation: $colour_saturation/$baseline_colour_saturation=$colour_saturation_variation"

	#% increase = [(New number – Original number)/Original number] x 100

	if [[ $((nr_colours)) -eq 1 ]]; then
		echo "Float Vanished."
		break
	fi

	if [[ $((white - baseline_white)) -gt 50 ]]; then
		echo "Threshold triggered..."
		click_float
		break
	fi
done

