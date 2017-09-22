#!/usr/bin/env python
#
# 2017-8-29 by NewDream
#
# i2c interaction with sound adc to extract level

"""
Call souldlevel_read() to fetch dB of sound
"""

import time
import pigpio

BUS = 1
SOUNDLEVEL_ADDR = 0x48

def soundlevel_read():
    """
    read soundlevel from i2c bus
    return soundlevel measurement in unit dB
    """
    # bus.write_i2c_block_data(SHT_ADDR, 0x24, [0x00])
    # time.sleep(0.1)
    # data = range(9)
    # for i in range(9):
    #     data[i] = bus.read_byte(VOC_ADDR)
    pi = pigpio.pi()
    if not pi.connected:
        return -1

    handle = pi.i2c_open(BUS, SOUNDLEVEL_ADDR)
    pi.i2c_write_device(handle, [0x02])

    samples = 100

    (count, data) = pi.i2c_read_device(handle, samples+1)
    # print "%d %d %d %d %d %d %d %d" % (data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]) # data[0] is adc from last sample, ignore
    pi.i2c_close(handle)

    soundlevel = sum(data[1:])/samples
    time.sleep(0.01)
    pi.stop()
    return soundlevel

if __name__ == "__main__":

    a = range(0,5)
    while 1:
        a[0] = soundlevel_read()
        time.sleep(0.1)
        a[1] = soundlevel_read()
        time.sleep(0.1) 
        a[2] = soundlevel_read()
        time.sleep(0.1)
        a[3] = soundlevel_read()
        time.sleep(0.1)
        a[4] = soundlevel_read()
        print sum(a)/5
