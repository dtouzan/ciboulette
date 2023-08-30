#!/bin/bash

###############################################################################
# Head
###############################################################################
cat ~/RASPICAM/name.txt
cat ~/RASPICAM/copyright.txt
name=$1
gain=$2
echo "Gain: $gain Exposition: 10s"

###############################################################################
# Cmos
###############################################################################
if [ ! -z $1 ]
then
    for i in 1 2 3 4 5 6 7 8 9 10
    do
        info=`date +%s`
        echo "$i: $1-$info-10s.dng"
        raspistill -t 1000 -n -md 3 -bm -ex off -ag $gain -ss 10000000 -st -awb off -r -q 100 -o $name-$info-10s.dng
        echo "."
        sleep 8
    done
fi