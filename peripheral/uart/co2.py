import RPi.GPIO as GPIO
import time
import serial
# under /dev there should be serial0->ttyS0, if not, run sodu raspi-config
# RESET and SET should be configured when rpi booting up

def co2_init():
    PIN_PM25_SET = 7
    PIN_RESET = 12
    PIN_SW_B = 16
    PIN_SW_A = 15
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # func = GPIO.gpio_function(PIN_RESET);
    # print func
    #if func != GPIO.OUT:

    GPIO.setup(PIN_RESET,GPIO.OUT)
    GPIO.output(PIN_RESET,GPIO.HIGH)
   
    # GPIO.setup(PIN_PM25_SET,GPIO.OUT)
    # GPIO.output(PIN_PM25_SET,GPIO.LOW)

    GPIO.setup(PIN_SW_B,GPIO.OUT)
    GPIO.output(PIN_SW_B,GPIO.LOW)

    GPIO.setup(PIN_SW_A,GPIO.OUT)
    GPIO.output(PIN_SW_A,GPIO.HIGH)

    ser = serial.Serial(
	port='/dev/serial0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1)
    time.sleep(0.01)
    ser.flushInput()
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

def co2_close(ser):
    ser.close()

if __name__ == "__main__":
    ser = co2_init()
    time.sleep(2)
    print "CO2 = %d" % co2_read(ser)
    time.sleep(1)
    print "CO2 = %d" % co2_read(ser)
    time.sleep(1)
    print "CO2 = %d" % co2_read(ser)
    co2_close(ser)
