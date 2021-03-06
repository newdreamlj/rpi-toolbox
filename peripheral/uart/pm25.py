import RPi.GPIO as GPIO
import time
import serial
# under /dev there should be serial0->ttyS0, if not, run sodu raspi-config
# RESET and SET should be configured when rpi booting up

def pm25_init():
    PIN_SET = 7
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

    GPIO.setup(PIN_SET,GPIO.OUT)
    GPIO.output(PIN_SET,GPIO.HIGH)

    GPIO.setup(PIN_SW_B,GPIO.OUT)
    GPIO.output(PIN_SW_B,GPIO.LOW)

    GPIO.setup(PIN_SW_A,GPIO.OUT)
    GPIO.output(PIN_SW_A,GPIO.LOW)

    ser = serial.Serial(
	port='/dev/serial0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1)
    time.sleep(0.02)    
    ser.flushInput()
    time.sleep(0.02)
    return ser

def pm25_read(ser):
    try:                        # stops program failing if no serial data
        response = ser.read(32)  # read 3 lines of serial port data

        pm25 = (ord(response[12])<<8) + ord(response[13])
        crc = (ord(response[30])<<8) + ord(response[31])
        crcx = 0
        for i in range(30):
            crcx = crcx + ord(response[i])
        if crc != crcx:
            print "Wrong CRC (%d but %D)" %(crc,crcx)
            return -1
        else:
	    pm25 = (ord(response[12])<<8) + ord(response[13])
            # print "PM 2.5 = %d" % pm25
            return pm25
    except Exception, e:
	print e
	ser.close()
        return -1
	# x=ser.readall()

def pm25_close(ser):
    ser.close()

if __name__ == "__main__":
    ser = pm25_init()
    time.sleep(2)
    print "PM2.5 = %d" % pm25_read(ser)
    time.sleep(2)
    print "PM2.5 = %d" % pm25_read(ser)
    time.sleep(2)
    print "PM2.5 = %d" % pm25_read(ser)
    pm25_close(ser)
