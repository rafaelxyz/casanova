#!/bin/python3
from __future__ import division

import RPi.GPIO as GPIO
import time
import os
import signal
import sys

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
PIN = 21
GPIO.setup(PIN, GPIO.OUT) # GPIO Assign mode
GPIO.setwarnings(False)

def signal_term_handler(signal, frame):
    GPIO.output(PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)
while True:
    GPIO.output(PIN, GPIO.HIGH)
