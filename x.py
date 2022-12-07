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

incorrect_state = False

def trigger_relay():
    try:
        while True:
            GPIO.output(PIN, GPIO.HIGH)
    except KeyboardInterrupt:
        GPIO.output(PIN, GPIO.LOW)

def check_input(char, text):
    global incorrect_state
    if re.match('[a-zA-Z]', char):
        if incorrect_state is True:
            text = ""
            incorrect_state = False
        text += char
    elif text.lower() == "casanova":
        text = "* correct *"
    elif len(text) >= 12:
        text = ""
    elif char == "\n":
        if len(text) > 0 and incorrect_state is False:
            text = " incorrect!"
            incorrect_state = True
        else:
            incorrect_state = False
            text = ""
    elif char == "\x7f" or char == "\x1b":
        text = text[:-1]
    return text

def display_txt(text):
    draw.text((x, top+8), str(text), font=font, fill=255)
    disp.image(image)
    disp.display()

def clear_screen():
    draw.rectangle((0,0,width,height), outline=0, fill=0)

txt = ""
while True:
    try:
        clear_screen()
        txt = check_input(sys.stdin.read(1)[0], txt)
        display_txt(txt)
        time.sleep(.1)
        if txt == "* correct *":
            GPIO.output(PIN, GPIO.HIGH)
            counter = 0
            while True:  # try removing while
                if sys.stdin.read(1)[0] == "\n":
                    GPIO.output(PIN, GPIO.LOW)
                    clear_screen()
                    break

    except(KeyboardInterrupt):
        GPIO.output(PIN, GPIO.LOW)
        print("\n")
        break

GPIO.cleanup()
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)
