import time
import sys
import os
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'drive')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from drive import SSD1305

from PIL import Image,ImageDraw,ImageFont

import subprocess

disp = SSD1305.SSD1305()
disp.Init()
logging.info("clear display")
disp.clear()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = 0
top = padding
bottom = height-padding
x = 0

font = ImageFont.truetype('04B_08__.TTF',16)

def draw_text(text):
    print(text)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top+8), str(text), font=font, fill=255)
    disp.getbuffer(image)
    disp.ShowImage()


def draw_inverted_text(text):
    print("!" + text)
    draw.rectangle((0,0,width,height), outline=0, fill=255)
    draw.text((x, top+8), str(text), font=font, fill=0)
    disp.getbuffer(image)
    disp.ShowImage()
