from __future__ import division

import time
import sys
sys.path.append('./drive')
import SPI
import SSD1305

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

##
import RPi.GPIO as GPIO
import os
import shutil
from threading import Thread
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

# Load default font.
#font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('04B_08__.TTF',8)

# def trigger_relay():
#     try:
#         while True:
#             GPIO.output(PIN, GPIO.HIGH)
#     except KeyboardInterrupt:
#         GPIO.output(PIN, GPIO.LOW)
#     finally:
#         GPIO.cleanup()

#         intxt = input()
#         if intxt == "c":
#             trigger_relay()
#         if intxt == "e":
#         else:
#             intxt = "incorrect"
#             time.sleep(3)

intxt = "incorrect"

def get_intxt():
    try:
        while True:
            intxt = input()
    except KeyboardInterrupt:
        break

t = Thread(target=get_intxt)
t.run()

while True:
    try:
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top+8), intxt, font=font, fill=255)
        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(.1)
    except(KeyboardInterrupt):
        print("\n")
        break
