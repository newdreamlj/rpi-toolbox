import RPi.GPIO as GPIO
import time


def pir_read():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(29,GPIO.IN)
    human_detected = 1 - GPIO.input(29)
    return human_detected

if __name__ == "__main__":

    while 1:
        human_detected = pir_read()
        if human_detected:
            print "Y"
        else:
            print "."
        time.sleep(1)
