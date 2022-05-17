#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# libraries
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

for pin in StepPins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)
