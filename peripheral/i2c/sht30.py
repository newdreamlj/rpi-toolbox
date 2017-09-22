#!/usr/bin/env python
#
# 2017-09-22 by NewDream
#
# i2c interaction with SHT30


"""

"""

import time
import pigpio

BUS = 1
SHT_ADDR = 0x44

def sht_read():
    pi = pigpio.pi()
    handle = pi.i2c_open(BUS, SHT_ADDR)
    # pi.write_i2c_block_data(SHT_ADDR, 0x24, [0x00])
    # time.sleep(0.01)
    # data = pi.i2c_read_i2c_block_data(SHT_ADDR, 0,6)
    pi.i2c_write_device(handle, [0x2c, 0x06])
    (count, data) = pi.i2c_read_device(handle, 6)
    temp = ((( (data[0]) * 256.0 + (data[1])) * 175 ) / 65535.0) - 45
    humid = ((( (data[3]) * 256.0 + (data[4])) * 100 ) / 65535.0)

    pi.i2c_close(handle)

    return temp,humid

if __name__ == "__main__":
    temp,humid = sht_read()
    print "T = %.2f, H = %.2f%%" % (temp,humid)

    time.sleep(1)
    temp,humid = sht_read()
    print "T = %.2f, H = %.2f%%" % (temp,humid)

    time.sleep(1)
    temp,humid = sht_read()
    print "T = %.2f, H = %.2f%%" % (temp,humid)

    time.sleep(1)
    temp,humid = sht_read()
    print "T = %.2f, H = %.2f%%" % (temp,humid)

    time.sleep(1)
    temp,humid = sht_read()
    print "T = %.2f, H = %.2f%%" % (temp,humid)

