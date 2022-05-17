#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# libraries
import time
import sys
import RPi.GPIO as GPIO

# Use BCM GPIO references
# Instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO signals to use Pins 
# Broche - GPIO
# 18     - GPIO24
# 22     - GPIO25
# 24     - GPIO8
# 26     - GPIO7
GPIO07 = 7
GPIO08 = 8
GPIO24 = 24
GPIO25 = 25
StepPins = [GPIO24,GPIO25,GPIO08,GPIO07]

# Set all pins as output
for pin in StepPins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)

# Define time delay between steps
WaitTime = 0.002 #set speed

# Define step degree
step_degree = 2048/360

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

# Step motor
def steps(nb):
        StepCounter = 0
        if nb<0: sign=-1
        else: sign=1
        nb=sign*nb*2 #times 2 because half-step
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

# Speed
def wait_time(waittime = 2):
    speed = waittime / 1000
    if waittime < 1:
        speed = 0.001  
    return speed

# degree rotate
def degree_rotate(degree = 0):
    rotate = int(degree)
    if degree < 0 :
        rotate = 0
    return rotate
    
# Main program
# ./SA200Motor.py +Degree speed
if __name__ == '__main__' :
    # Start main loop
    nbStepsPerRev = degree_rotate(int(sys.argv[1])) 
    WaitTime = wait_time(int(sys.argv[2]))
    hasRun=False         
    while not hasRun:
            steps(nbStepsPerRev)
            time.sleep(1)
            hasRun=True

    for pin in StepPins:
            GPIO.output(pin, False)
