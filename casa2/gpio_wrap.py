import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
PIN = 21
GPIO.setup(PIN, GPIO.OUT) # GPIO Assign mode
GPIO.setwarnings(False)

INVERT = False

def set_high():
    if not INVERT:
        GPIO.output(PIN, GPIO.HIGH)
    else:
        GPIO.output(PIN, GPIO.LOW)

def set_low():
    if not INVERT:
        GPIO.output(PIN, GPIO.LOW)
    else:
        GPIO.output(PIN, GPIO.HIGH)

def cleanup():
    GPIO.cleanup()
