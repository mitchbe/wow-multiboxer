#!/bin/bash


function screenshot() {
	xwd -id $WIN_ID | convert xwd:- out/screenshot.png
}

COMBAT_ICON_BOX_FULLSCRN='24x21+30+74' 
COMBAT_ICON_BOX_HALFSCRN='15x30+15+73'

function test_combat() {

	xwd -id $WIN_ID | \
	convert xwd:- -crop "$COMBAT_ICON_BOX_FULLSCRN" \
		\( -map combaticon_pallette.png \) miff:- | \
	convert miff:- -format %c histogram:info:- | grep red | wc -l
}

HEALTHBAR_BOX_FULLSCRN='143x2+117+60'

function get_health() {
	#histogram=$( xwd -id $WIN_ID | \
	#convert xwd:- -crop "$HEALTHBAR_BOX_FULLSCRN" \
	#	\( -gamma 3 \) \
	#	\( -map healthbox_pallette.png \) miff:- | \
	#	convert miff:- -format %c histogram:info:-) 

	xwd -id $WIN_ID | \
	convert xwd:- -crop "$HEALTHBAR_BOX_FULLSCRN" out/h$1.png
	convert out/h$1.png -channel G -separate out/h$1g.png
	convert out/h$1g.png -brightness-contrast 10,50 out/h$1b.png
	#convert out/h$1b.png -colors 2 -colorspace gray  -normalize  out/h$1f.png  
	convert	out/h$1b.png -map bnw_pallette.png out/h$1f.png 
	#convert	out/h$1.png -map healthbox_pallette.png out/hb$1.png 
	#convert	bright 10 contr 50 out/h$1.png -map healthbox_pallette.png out/hb$1.png 

	histogram=$(convert out/h$1f.png -format %c histogram:info:-) 
	#echo -e "$histogram"
	lime=$(($(echo -e "$histogram" | grep "FFFFFF" | awk '{print $1}'| sed 's:.$::')))
	black=$(($(echo -e "$histogram" | grep "000000" | awk '{print $1}'| sed 's:.$::')))
	hp_tot=$(($lime+$black))
	#echo "Lime/black: $lime/$black"
	if [[ hp_tot -eq 0 ]]; then
		echo "N/A"
		#rm out/h$1.png
		#rm out/hb$1.png
		#rm out/h$1.png
		#rm out/h$1g.png
		#rm out/h$1b.png
		#rm out/h$1f.png
		return
	fi

	hp_perc=$(echo "$lime / $hp_tot * 100" | bc -l | xargs printf %.2f)
	echo "$hp_perc"
}


WIN_ID=$(xwininfo -name "World of Warcraft" | grep "Window id" | cut -d ' ' -f 4 )
rm out/*
screenshot
isCombat=$(test_combat)
echo "Player in combat: $isCombat"

i=0
while true
do
	i=$(($i+1))
	get_health $i
	sleep 1
	#break;
done

#histogram=$( xwd -id $WIN_ID | \
#convert xwd:- -crop "$HEALTHBAR_BOX_FULLSCRN" \
#	\( -map healthbox_pallette.png \) miff:- | \
#	convert miff:- -format %c histogram:info:-) 

#echo "Histogram is: "
#echo $histogram


#echo "identify -precision 5 -define identify:locate=maximum -define identify:limit=3 out/tmpx.png" 

#DO_WIN_ID=$(xdotool search --name "World of Warcraft")
#echo "win id: $DO_WIN_ID"


#echo "convert out/snap.bmp -crop '15x30+15+73' out/a.png"

#convert histogram:red-combat.png -format %c histogram:info:-
