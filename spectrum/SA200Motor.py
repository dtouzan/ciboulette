#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# libraries
import time
import RPi.GPIO as GPIO
# Use BCM GPIO references
# Instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
# Define GPIO signals to use Pins 18,22,24,26 GPIO24,GPIO25,GPIO8,GPIO7
# Define GPIO signals to use Pins 16,18,24,26 GPIO23,GPIO24,GPIO8,GPIO7
StepPins = [24,25,8,7]
# Set all pins as output
for pin in StepPins:
        print("Setup pins")
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, False)
# Define time delay between steps
WaitTime = 0.001 #set speed
# Define simple sequence
StepCount1 = 4
Seq1 = []
Seq1 = [i for i in range(0, StepCount1)]
Seq1[0] = [1,0,0,0]
Seq1[1] = [0,1,0,0]
Seq1[2] = [0,0,1,0]
Seq1[3] = [0,0,0,1]
# Define advanced half-step sequence
StepCount2 = 8
Seq2 = []
Seq2 = [i for i in range(0, StepCount2)]
Seq2[0] = [1,0,0,0]
Seq2[1] = [1,1,0,0]
Seq2[2] = [0,1,0,0]
Seq2[3] = [0,1,1,0]
Seq2[4] = [0,0,1,0]
Seq2[5] = [0,0,1,1]
Seq2[6] = [0,0,0,1]
Seq2[7] = [1,0,0,1]
# Choose a sequence to use
Seq = Seq2
StepCount = StepCount2
def steps(nb):
        StepCounter = 0
        if nb<0: sign=-1
        else: sign=1
        nb=sign*nb*2 #times 2 because half-step
        print("nbsteps {} and sign {}".format(nb,sign))
        for i in range(nb):
                for pin in range(4):
                        xpin = StepPins[pin]
                        if Seq[StepCounter][pin]!=0:
                                GPIO.output(xpin, True)
                        else:
                                GPIO.output(xpin, False)
                StepCounter += sign
        # If we reach the end of the sequence
        # start again
                if (StepCounter==StepCount):
                        StepCounter = 0
                if (StepCounter<0):
                        StepCounter = StepCount-1
                # Wait before moving on
                time.sleep(WaitTime)

if __name__ == '__main__' :
    # Variable 
    import sys
    _dg = int(sys.argv[1])
    if _dg > 360 :
        _dg = 360
    if _dg < -360 :
        _dg = -360

    # Start main loop
    # nbStepsPerRev=2048 full rotate
    _1d = 2048/360
    rot = int(_dg*_1d)
    print(str(_dg)+"°:",rot)
    nbStepsPerRev=rot    
    hasRun=False
    while not hasRun:
            steps(nbStepsPerRev)# parcourt un tour dans le sens horaire
            time.sleep(1)
            #steps(-nbStepsPerRev)# parcourt un tour dans le sens anti-horaire
            #time.sleep(1)
            hasRun=True
    print("Stop motor")
    for pin in StepPins:
            GPIO.output(pin, False)