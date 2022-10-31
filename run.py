#!/bin/python3
from __future__ import division

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
PIN = 21
GPIO.setup(PIN, GPIO.OUT) # GPIO Assign mode
GPIO.setwarnings(False)

dir = os.environ['HOME'] + "/casanova/"

def set_color(color):
    os.system(dir + "colors.sh " + color)

def input_password():
    try:
        while True:
            set_color("black")
            x = input("")
            if x == "casanova!" or x == "c":
                set_color("green")
                print("correct password")
                trigger_relay()
            if x == "exit123" or x == "e":
                set_color("black")
                print("exiting!")
                GPIO.cleanup()
                exit(0)
            else:
                set_color("red")
                print("wrong password, try again")
                time.sleep(3)
    except KeyboardInterrupt:
        set_color("black")
        print("wrong password, try again")
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
