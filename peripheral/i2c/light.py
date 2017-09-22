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
LIGHT_ADDR = 0x48

def light_read():
    """
    read light from i2c bus
    return light measurement in unit dB
    """
    # bus.write_i2c_block_data(SHT_ADDR, 0x24, [0x00])
    # time.sleep(0.1)
    # data = range(9)
    # for i in range(9):
    #     data[i] = bus.read_byte(VOC_ADDR)
    pi = pigpio.pi()
    if not pi.connected:
        return -1

    handle = pi.i2c_open(BUS, LIGHT_ADDR)
    pi.i2c_write_device(handle, [0x00])

    samples = 20

    (count, data) = pi.i2c_read_device(handle, samples+1)
    # print "%d %d %d %d %d %d %d %d" % (data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]) # data[0] is adc from last sample, ignore
    pi.i2c_close(handle)

    light = sum(data[1:])/samples
    time.sleep(0.01)
    pi.stop()
    return light

if __name__ == "__main__":

    while 1:
        light = light_read()
        print "light = %d" % light
        time.sleep(1)
