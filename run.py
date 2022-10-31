#!/bin/python3
from __future__ import division

import RPi.GPIO as GPIO
import time
import os
import shutil

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
PIN = 21
GPIO.setup(PIN, GPIO.OUT) # GPIO Assign mode
GPIO.setwarnings(False)

os.environ["PS1"] = "\e[?1;2;32;c"
columns = shutil.get_terminal_size().columns

def bgcolor(color):
    os.system("/home/casanova/casanova/colors.sh " + color)

def txt(text):
    print("\n\n\n" + text.center(columns))

def input_password():
    try:
        while True:
            bgcolor("black")
            x = input("")
            if x == "casanova!" or x == "c":
                bgcolor("green")
                txt("correct password")
                trigger_relay()
            if x == "exit123" or x == "e":
                bgcolor("black")
                txt("exiting!")
                GPIO.cleanup()
                exit(0)
            else:
                bgcolor("red")
                txt("wrong password, try again")
                time.sleep(3)
    except KeyboardInterrupt:
        bgcolor("black")
        txt("wrong password, try again")
        input_password()


def trigger_relay():
    try:
        while True:
            GPIO.output(PIN, GPIO.HIGH)
            #txt('pin21 on')
            time.sleep(1)
            GPIO.output(PIN, GPIO.LOW)
            #txt('pin21 off')
            time.sleep(1)
    except KeyboardInterrupt:
        input_password()
    finally:
        GPIO.cleanup()

input_password()
