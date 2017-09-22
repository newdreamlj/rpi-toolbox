#!/usr/bin/env python
#
# 2017-4-19 by NewDream
#
# i2c interaction with ADXl345


import smbus
import time
import ctypes

bus = smbus.SMBus(1)
ADXL_ADDR = 0x53

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

def adxl_init():
    bus.write_byte_data(ADXL_ADDR,DATA_FORMAT,0x28)
    bus.write_byte_data(ADXL_ADDR,BW_RATE,0x09)
    bus.write_byte_data(ADXL_ADDR,FIFO_CTL,0x8f)
    bus.write_byte_data(ADXL_ADDR,POWER_CTL,0x28)
    bus.write_byte_data(ADXL_ADDR,INT_ENABLE,0x00)
    bus.write_byte_data(ADXL_ADDR,OFSX,0x00)
    bus.write_byte_data(ADXL_ADDR,OFSY,0x00)
    bus.write_byte_data(ADXL_ADDR,OFSZ,0x00)

def adxl_read():
    for i in range(320):
        # bus.write_byte(ADXL_ADDR, 0x32)
        data = bus.read_i2c_block_data(ADXL_ADDR, 0x32, 6)
        dx = ctypes.c_int16((data[1]<<8) + data[0]).value * 4
        dy = ctypes.c_int16((data[3]<<8) + data[2]).value * 4
        dz = ctypes.c_int16((data[5]<<8) + data[4]).value * 4
        print "dx = %5d   dy = %5d   dz = %5d" % (dx,dy,dz)

if __name__ == "__main__":
    adxl_init()
    time.sleep(0.5)
    adxl_read()

