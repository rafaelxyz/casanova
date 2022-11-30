import re
import tty, sys, termios

filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)

def check_input(char, text):
    if re.match('[a-zA-Z]', char):
        text += char
    if text.lower() == "casanova":
        text = "* correct *"
    elif char == "\n":
        text = ""
    return text


txt = ""
while True:
    #txt = check_input(sys.stdin.read(1)[0], txt)
    #print(txt)
    x = sys.stdin.read(1)[0]
    print(repr(x))

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)
