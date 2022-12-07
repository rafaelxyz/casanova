from __future__ import division

import time
import sys
sys.path.append('./drive')
import SPI
import SSD1305

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

##
import RPi.GPIO as GPIO
import os
import shutil
import subprocess
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
PIN = 21
GPIO.setup(PIN, GPIO.OUT) # GPIO Assign mode
GPIO.setwarnings(False)
##

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 24
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware SPI:
disp = SSD1305.SSD1305_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 0
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('04B_08__.TTF',16)

import re
import tty, sys, termios

filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)

def trigger_relay():
    try:
        while True:
            GPIO.output(PIN, GPIO.HIGH)
    except KeyboardInterrupt:
        GPIO.output(PIN, GPIO.LOW)

def draw_text(text):
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top+8), str(text), font=font, fill=255)
    disp.image(image)
    disp.display()

def draw_blink_text(text):
    counter = 0
    while True:
        counter = counter + 1
        if counter % 2:
            draw_text(text)
        else:
            draw_text("")
        time.sleep(1)
        if counter == 10:
            counter = 0

def update_txt(char, text):
    global state
    if state == checking:
        if re.match('[a-zA-Z]', char):
            text += char
        if text.lower() == "casanova":
            state = correct
        if text.lower() == "szcz":
            state = shutdown
        elif char == "\x7f" or char == "\x1b":
            text = text[:-1]
        elif char == "\n" and len(text) > 0:
            state = incorrect
            text = ""
        elif len(text) > 11:
            state = incorrect
            text = ""
    return text

def statem():
    global state
    if state == starting:
        draw_text("> started")
        state = checking
    elif state == checking:
        pass
    elif state == correct:
        draw_text("* correct *")
    elif state == incorrect:
        draw_text("incorrect!")
        time.sleep(3)
        state = checking
    elif state == shutdown:
        draw_text("< shutdown ")
        GPIO.cleanup()
        subprocess.call(['shutdown', '-h', 'now'], shell=False)

starting, checking, correct, incorrect, shutdown = range(5)
state = starting
txt = ""

statem()

while True:
    try:
        char = sys.stdin.read(1)[0]
        txt = update_txt(char, txt)
        draw_text(txt)
        statem()
        time.sleep(.1)
        if state == correct:
            while True:
                GPIO.output(PIN, GPIO.HIGH)
                if sys.stdin.read(1)[0] == "1":
                    GPIO.output(PIN, GPIO.LOW)
                    txt = ""
                    state = starting
                    break

    except(KeyboardInterrupt):
        GPIO.output(PIN, GPIO.LOW)
        draw_text("x <Enter>")
        print("exiting to terminal")
        break

GPIO.cleanup()
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)
