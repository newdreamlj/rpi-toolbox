import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.IN)

while 1:
    #input value from Pin 11
    human_detected = GPIO.input(12)

    if human_detected:
        GPIO.output(11,GPIO.LOW)
    else:
        GPIO.output(11,GPIO.HIGH)

    time.sleep(0.1)
