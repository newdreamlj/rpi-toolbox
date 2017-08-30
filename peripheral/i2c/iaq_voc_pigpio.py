#!/usr/bin/env python
#
# 2017-8-29 by NewDream
#
# i2c interaction with IAQ-CORE VOC


import smbus
import time
import pigpio

BUS = 1
VOC_ADDR = 0x5A
pi = pigpio.pi()

def voc_read():
    # bus.write_i2c_block_data(SHT_ADDR, 0x24, [0x00])
    # time.sleep(0.1)
    # data = range(9)
    # for i in range(9):
    #     data[i] = bus.read_byte(VOC_ADDR)
    handle = pi.i2c_open(BUS, VOC_ADDR)
    (count, data) = pi.i2c_read_device(handle, 9)
    pi.i2c_close(handle)
 
    pred = ((data[0]) << 8) + (data[1])
    status = (data[2])
    resistance = ((data[3]) << 24) + ((data[4]) << 16) + ((data[5]) << 8) + (data[6])
    tvoc = ((data[7]) << 8) + (data[8])

    print "pred = %6d  stats = %6d  resi = %d tvoc = %d" % (pred,status,resistance,tvoc)

if __name__ == "__main__":
    voc_read()
    time.sleep(1)
    voc_read()
    time.sleep(1)
    voc_read()
