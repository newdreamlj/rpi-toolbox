#!/usr/bin/env python
#
# 2017-4-19 by NewDream
#
# i2c interaction with ADXl345


import smbus
import time
import ctypes


DEVICE_ID       =0x00
THRESH_TAP      =0x1D
OFSX            =0x1E
OFSY            =0x1F
OFSZ            =0x20
DUR             =0x21
Latent          =0x22
Window          =0x23
THRESH_ACT      =0x24
THRESH_INACT    =0x25
TIME_INACT      =0x26
ACT_INACT_CTL   =0x27
THRESH_FF       =0x28
TIME_FF         =0x29
TAP_AXES        =0x2A
ACT_TAP_STATUS  =0x2B
BW_RATE         =0x2C
POWER_CTL       =0x2D

INT_ENABLE      =0x2E
INT_MAP         =0x2F
INT_SOURCE      =0x30
DATA_FORMAT     =0x31
DATA_X0         =0x32
DATA_X1         =0x33
DATA_Y0         =0x34
DATA_Y1         =0x35
DATA_Z0         =0x36
DATA_Z1         =0x37
FIFO_CTL        =0x38
FIFO_STATUS     =0x39


ADXL_ADDR = 0x53
class Adxl345(object):

    def __init__(self):
        self.i2c_address = ADXL_ADDR
        self.i2c_bus = smbus.SMBus(1)

    def init(self):
        # D7        | D6  | D5         | D4 |  D3      | D2      |   D1     D0
        # SELF_TEST | SPI | INT_INVERT | 0  | FULL_RES | Justify |    Range
        #                                      1 :full resolution    0     0   : 2 g
        #                                                            0     1   : 4 g
        #                                                            1     0   : 8 g
        #                                                            1     1   : 16 g

        self.i2c_bus.write_byte_data(ADXL_ADDR,DATA_FORMAT,0x28)
        self.i2c_bus.write_byte_data(ADXL_ADDR,BW_RATE,0x09)
        self.i2c_bus.write_byte_data(ADXL_ADDR,FIFO_CTL,0x8f)  # 10xx xxxx : streaming
        self.i2c_bus.write_byte_data(ADXL_ADDR,POWER_CTL,0x28)
        self.i2c_bus.write_byte_data(ADXL_ADDR,INT_ENABLE,0x00)
        self.i2c_bus.write_byte_data(ADXL_ADDR,OFSX,0x00)
        self.i2c_bus.write_byte_data(ADXL_ADDR,OFSY,0x00)
        self.i2c_bus.write_byte_data(ADXL_ADDR,OFSZ,0x00)
  
    def flash_fifo(self):
        try:
            for i in range(32):
                data = self.i2c_bus.read_i2c_block_data(ADXL_ADDR, 0x32, 6)
        except Exception, e:
            print "less than 32"
	    return

    def read(self):
        count = 0
        ax = 0
        ay = 0
        az = 0
        timestamp = int(time.time()*1e9)
        for i in range(5):
            # self.i2c_bus.write_byte(ADXL_ADDR, 0x32)
            try:
                data = self.i2c_bus.read_i2c_block_data(ADXL_ADDR, 0x32, 6)
                time.sleep(0.000005)
            except Exception, e:
                print "not enough points %d" % count
                break
            count = count + 1
            ax = ax + ctypes.c_int16((data[1]<<8) + data[0]).value * 9.8 / 250
            ay = ay + ctypes.c_int16((data[3]<<8) + data[2]).value * 9.8 / 250
            az = az + ctypes.c_int16((data[5]<<8) + data[4]).value * 9.8 / 250
        if count == 0:
            return 0,0,0,0
        ax = ax / count
        ay = ay / count
        az = az / count
        return ax,ay,az,timestamp
        # print "%d:  ax = %5d   ay = %5d   az = %5d" % (timestamp,ax,ay,az)
      
if __name__ == "__main__":
    adxl = Adxl345()
    adxl.init()
    time.sleep(0.5)
    adxl.flash_fifo()

    for i in range(50): 
        dx,dy,dz,timestamp = adxl.read()
        print "%d:  dx = %5d   dy = %5d   dz = %5d" % (timestamp,dx,dy,dz)
        time.sleep(0.1)

