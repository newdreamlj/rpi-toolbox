#!/usr/bin/env python
#
# 2017-8-29 by NewDream
#
# i2c interaction with IAQ-CORE VOC

"""
5 minutes for warming-up after power on
During warming-up, status equals 2 and tvoc equals -2

Call tvoc_read() to fetch status and tvoc
"""

import time
import pigpio

BUS = 1
VOC_ADDR = 0x5A

def tvoc_read():
    """
    read voc from i2c bus
    return status and tvoc measurement
    status:
	0x00: OK (data valid)
	0x10: RUNIN (module in warm up phase) 
	0x01: BUSY (re-read multi byte data!) 
	0x80: ERROR (if constant: replace sensor)
   tvoc:
	Prediction (TVOC eq. ppb)
    """
    # bus.write_i2c_block_data(SHT_ADDR, 0x24, [0x00])
    # time.sleep(0.1)
    # data = range(9)
    # for i in range(9):
    #     data[i] = bus.read_byte(VOC_ADDR)
    pi = pigpio.pi()
    handle = pi.i2c_open(BUS, VOC_ADDR)
    (count, data) = pi.i2c_read_device(handle, 9)
    pi.i2c_close(handle)
 
    # pred = ((data[0]) << 8) + (data[1])
    status = (data[2])
    # resistance = ((data[3]) << 24) + ((data[4]) << 16) + ((data[5]) << 8) + (data[6])
    tvoc = ((data[7]) << 8) + (data[8])

    if status!=0:
        tvoc = -status
    return status, tvoc

if __name__ == "__main__":
    status, tvoc = tvoc_read()
    print "tvoc = %d" % tvoc
    time.sleep(1)
    status, tvoc = tvoc_read()
    print "tvoc = %d" % tvoc
    time.sleep(1)
    status, tvoc = tvoc_read()
    print "tvoc = %d" % tvoc
    time.sleep(1)
    status, tvoc = tvoc_read()
    print "tvoc = %d" % tvoc
    time.sleep(1)
    status, tvoc = tvoc_read()
    print "tvoc = %d" % tvoc


