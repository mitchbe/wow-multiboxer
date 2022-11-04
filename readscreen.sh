#!/bin/bash


function screenshot() {
	xwd -id $WIN_ID | convert xwd:- out/screenshot.png
}

COMBAT_ICON_BOX_FULLSCRN='26x20+30+74' 
COMBAT_ICON_BOX_HALFSCRN='15x30+15+73'

function test_combat() {
# composite out/baseline.bmp xwd:- -compose difference
#convert out/screenshot.png -crop '26x20+30+74' -colorspace gray -brightness-contrast 0,50  out/tmp.png
 	
	local tmp="$(mktemp -p $dir)"

	result=$(convert miff:$img -crop "$COMBAT_ICON_BOX_FULLSCRN" \
		-colorspace gray -brightness-contrast 0,50 miff:- | \
	composite kombaticon.png miff:- -compose difference miff:- | \
	convert	miff:- -map pallettes/bnw_pallette.png miff:- |
	convert miff:- -format %c histogram:info:- | grep "#FFFFFF" | awk '{print $1}'| sed 's:.$::')
	
	result=$(($result))
	if [[ result -gt 10 ]]; then
		echo "false"
		return
	fi
	echo "true"



	#histogram=$(convert miff:$tmp -format %c histogram:info:-) 
	#echo -e "$histogram"

	#convert miff:- -format %c histogram:info:- | grep red | wc -l
	#convert miff:- -map pallettes/bnw_pallette.png miff:-


	#convert miff:$img -crop "$COMBAT_ICON_BOX_FULLSCRN" \
	#	\( -map pallettes/combaticon_pallette.png \) miff:- | \
	#convert miff:- -format %c histogram:info:- | grep red | wc -l
}

HEALTHBAR_BOX_FULLSCRN='143x2+117+60'

function get_health() {
	#histogram=$( xwd -id $WIN_ID | \
	#convert xwd:- -crop "$HEALTHBAR_BOX_FULLSCRN" \
	#	\( -gamma 3 \) \
	#	\( -map healthbox_pallette.png \) miff:- | \
	#	convert miff:- -format %c histogram:info:-) 
	#convert out/h$1b.png -colors 2 -colorspace gray  -normalize  out/h$1f.png  
	#convert	out/h$1.png -map healthbox_pallette.png out/hb$1.png 
	#convert	bright 10 contr 50 out/h$1.png -map healthbox_pallette.png out/hb$1.png 

	local tmp="$(mktemp -p $dir)"

	convert miff:$img -crop "$HEALTHBAR_BOX_FULLSCRN" miff:- | \
	convert miff:- -channel G -separate miff:- | \
	convert miff:- -brightness-contrast 10,50 miff:- | \
	convert	miff:- -map pallettes/bnw_pallette.png miff:$tmp
	histogram=$(convert miff:$tmp -format %c histogram:info:-) 

	local lime=$(($(echo -e "$histogram" | grep "FFFFFF" | awk '{print $1}'| sed 's:.$::')))
	local black=$(($(echo -e "$histogram" | grep "000000" | awk '{print $1}'| sed 's:.$::')))
	local hp_tot=$(($lime+$black))
	#echo "Lime/black: $lime/$black"
	if [[ hp_tot -eq 0 ]]; then
		echo "-"
		return
	fi
	hp_perc=$(echo "$lime / $hp_tot * 100" | bc -l | xargs printf %.2f)
	echo "$hp_perc"
}


#WIN_ID=$(xwininfo -name "World of Warcraft" | grep "Window id" | cut -d ' ' -f 4 )
WIN_ID=$1
#rm out/*
screenshot

dir="/dev/shm/wowbot/"
rm -rf $dir 
mkdir $dir
img="$(mktemp -p $dir)"
#echo $img

xwd -id $WIN_ID | convert xwd:- miff:- >> $img
if [ $? -ne 0 ]; then
	jq -n "{nodata:1}"
	exit 0
fi
#convert miff:$img out/proof.png

isCombat=$(test_combat)
hp=$(get_health)
#echo "Player in combat: $isCombat; HP: $hp"
jq -n "{in_combat:$isCombat, health:\"$hp\"}"


rm $img
