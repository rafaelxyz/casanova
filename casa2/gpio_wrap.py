import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
PIN = 21
GPIO.setup(PIN, GPIO.OUT) # GPIO Assign mode
GPIO.setwarnings(False)


def set_high():
    GPIO.output(PIN, GPIO.HIGH)

def set_low():
    GPIO.output(PIN, GPIO.LOW)

def cleanup():
    GPIO.cleanup()
