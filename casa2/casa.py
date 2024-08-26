import re
import tty
import sys
import termios
import time
import sys
import subprocess

import gpio_wrap
import draw_wrap

filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)


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
        draw_wrap.draw_text("> started")
        state = checking
    elif state == checking:
        pass
    elif state == correct:
        draw_wrap.draw_inverted_text(" * correct *")
    elif state == incorrect:
        draw_wrap.draw_inverted_text(" incorrect!")
        state = checking
    elif state == shutdown:
        draw_wrap.draw_text("< shutdown ")
        gpio_wrap.cleanup()
        subprocess.call(['shutdown', '-h', 'now'], shell=False)


starting, checking, correct, incorrect, shutdown = range(5)
state = starting
txt = ""

statem()

while True:
    try:
        char = sys.stdin.read(1)[0]
        txt = update_txt(char, txt)
        draw_wrap.draw_text(txt)
        statem()
        time.sleep(.1)
        if state == correct:
            while True:
                gpio_wrap.set_high()
                if sys.stdin.read(1)[0] == "1":
                    # '1' was pressed, reset the game
                    gpio_wrap.set_low()
                    txt = ""
                    state = starting
                    break

    except(KeyboardInterrupt):
        gpio_wrap.set_low()
        draw_wrap.draw_text("x <Enter>")
        print("exiting to terminal")
        break

gpio_wrap.cleanup()
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)
