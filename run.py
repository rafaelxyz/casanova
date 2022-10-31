#!/bin/python3
from __future__ import division

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
PIN = 21
GPIO.setup(PIN, GPIO.OUT) # GPIO Assign mode
GPIO.setwarnings(False)


def input_password():
    os.system("clear")
    try:
        while True:
            x = input("")
            if x == "casanova!" or x == "c":
                os.system("clear")
                os.system("./colors.sh green")
                print("correct password")
                trigger_relay()
            if x == "exit123" or x == "e":
                GPIO.cleanup()
                exit(0)
            else
                os.system("clear")
                os.system("./colors.sh red")
                print("wrong password")
                time.sleep(3)
    except KeyboardInterrupt:
        input_password()


def trigger_relay():
    try:
        while True:
            GPIO.output(PIN, GPIO.HIGH)
            #print('pin21 on')
            time.sleep(1)
            GPIO.output(PIN, GPIO.LOW)
            #print('pin21 off')
            time.sleep(1)
    except KeyboardInterrupt:
        input_password()
    finally:
        GPIO.cleanup()

input_password()
