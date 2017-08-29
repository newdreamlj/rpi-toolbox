import RPi.GPIO as GPIO
import time
import serial


def serial_init():
	global ser
	PIN_RESET = 12;
	GPIO.setmode(GPIO.BOARD)	
	GPIO.setwarnings(False)
	# func = GPIO.gpio_function(PIN_RESET);
	# print func
 	#if func != GPIO.OUT:
	GPIO.setup(PIN_RESET,GPIO.OUT)
	GPIO.output(PIN_RESET,GPIO.HIGH)
	ser = serial.Serial(
		port='/dev/serial1',
		baudrate = 9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1)

def serial_read():
	global ser
	try:                                       # stops program failing if no serial data
		response = ser.read(1)  # read 3 lines of serial port data
		print "%x" % response[0]
		ser.close()
	except Exception, e:
		print e
		ser.close()	
	# x=ser.readall()

if __name__ == "__main__":
	serial_init()
	serial_read()

