import RPi.GPIO as GPIO
import time
import serial

def co2_init():
    PIN_RESET = 12;
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # func = GPIO.gpio_function(PIN_RESET);
    # print func
    #if func != GPIO.OUT:
    GPIO.setup(PIN_RESET,GPIO.OUT)
    GPIO.output(PIN_RESET,GPIO.HIGH)
    ser = serial.Serial(
	port='/dev/serial0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1)
    return ser

def co2_read(ser):
    try:                        # stops program failing if no serial data
        cmd = bytearray([0x42,0x4d,0xe3,0x00,0x00,0x01,0x72])
        ser.write(cmd)
        time.sleep(0.01)
        response = ser.read(12)  # read 3 lines of serial port data
	co2 = (ord(response[4])<<8) + ord(response[5])
        # print "CO2 = %d" % co2
        return co2
    except Exception, e:
	print e
	ser.close()
        return -1
	# x=ser.readall()

if __name__ == "__main__":
    ser = co2_init()
    time.sleep(0.1)
    print "CO2 = %d" % co2_read(ser)
    time.sleep(1)
    print "CO2 = %d" % co2_read(ser)
    time.sleep(1)
    print "CO2 = %d" % co2_read(ser)
    ser.close()
