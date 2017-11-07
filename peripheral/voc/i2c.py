#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2017-4-19 by NewDream
#
# i2c interaction with SHT30


import smbus
import time

CMD_READ_SERIALNBR  = 0x3780  # read serial number
CMD_READ_STATUS     = 0xF32D  # read status register
CMD_CLEAR_STATUS    = 0x3041  # clear status register
CMD_HEATER_ENABLE   = 0x306D  # enabled heater
CMD_HEATER_DISABLE  = 0x3066  # disable heater
CMD_SOFT_RESET      = 0x30A2  # soft reset
CMD_MEAS_CLOCKSTR_H = 0x2C06  # measurement: clock stretching, high repeatability
CMD_MEAS_CLOCKSTR_M = 0x2C0D  # measurement: clock stretching, medium repeatability
CMD_MEAS_CLOCKSTR_L = 0x2C10  # measurement: clock stretching, low repeatability
CMD_MEAS_POLLING_H  = 0x2400  # measurement: polling, high repeatability
CMD_MEAS_POLLING_M  = 0x240B  # measurement: polling, medium repeatability
CMD_MEAS_POLLING_L  = 0x2416  # measurement: polling, low repeatability
CMD_MEAS_PERI_05_H  = 0x2032  # measurement: periodic 0.5 mps, high repeatability
CMD_MEAS_PERI_05_M  = 0x2024  # measurement: periodic 0.5 mps, medium repeatability
CMD_MEAS_PERI_05_L  = 0x202F  # measurement: periodic 0.5 mps, low repeatability
CMD_MEAS_PERI_1_H   = 0x2130  # measurement: periodic 1 mps, high repeatability
CMD_MEAS_PERI_1_M   = 0x2126  # measurement: periodic 1 mps, medium repeatability
CMD_MEAS_PERI_1_L   = 0x212D  # measurement: periodic 1 mps, low repeatability
CMD_MEAS_PERI_2_H   = 0x2236  # measurement: periodic 2 mps, high repeatability
CMD_MEAS_PERI_2_M   = 0x2220  # measurement: periodic 2 mps, medium repeatability
CMD_MEAS_PERI_2_L   = 0x222B  # measurement: periodic 2 mps, low repeatability
CMD_MEAS_PERI_4_H   = 0x2334  # measurement: periodic 4 mps, high repeatability
CMD_MEAS_PERI_4_M   = 0x2322  # measurement: periodic 4 mps, medium repeatability
CMD_MEAS_PERI_4_L   = 0x2329  # measurement: periodic 4 mps, low repeatability
CMD_MEAS_PERI_10_H  = 0x2737  # measurement: periodic 10 mps, high repeatability
CMD_MEAS_PERI_10_M  = 0x2721  # measurement: periodic 10 mps, medium repeatability
CMD_MEAS_PERI_10_L  = 0x272A  # measurement: periodic 10 mps, low repeatability
CMD_FETCH_DATA      = 0xE000  # readout measurements for periodic mode
CMD_R_AL_LIM_LS     = 0xE102  # read alert limits, low set
CMD_R_AL_LIM_LC     = 0xE109  # read alert limits, low clear
CMD_R_AL_LIM_HS     = 0xE11F  # read alert limits, high set
CMD_R_AL_LIM_HC     = 0xE114  # read alert limits, high clear
CMD_W_AL_LIM_HS     = 0x611D  # write alert limits, high set
CMD_W_AL_LIM_HC     = 0x6116  # write alert limits, high clear
CMD_W_AL_LIM_LC     = 0x610B  # write alert limits, low clear
CMD_W_AL_LIM_LS     = 0x6100  # write alert limits, low set
CMD_NO_SLEEP        = 0x303E


# set sht30 address according to hardware wiring, 0x44 or 0x45
SHT_ADDR = 0x44 

class Sht30(object):

    def __init__(self):
        self.i2c_address = SHT_ADDR
        self.i2c_bus = smbus.SMBus(1)

    def set_config(self,CONFIG_TO_SET):
        self.i2c_bus.write_i2c_block_data(self.i2c_address, CONFIG_TO_SET >> 8, [CONFIG_TO_SET & 0xff])

    def enable_periodic_measurement(self):
        self.set_config(CMD_MEAS_PERI_2_H)

    def read_single_shot(self):
        self.set_config(CMD_MEAS_PERI_2_H)
        timestamp = int(time.time()*1e9)
        try:
	    data = self.i2c_bus.read_i2c_block_data(SHT_ADDR, 0,6)
        except Exception, e:
            return 0,0,0
        temp = ((( data[0] * 256.0 + data[1]) * 175 ) / 65535.0) - 45
        humid = ((( data[3] * 256.0 + data[4]) * 100 ) / 65535.0)
        # print "T = %6.2f   RH = %6.2f %%" % (temp,humid)
        return temp,humid,timestamp

    def read_periodic(self):
        self.set_config(CMD_FETCH_DATA)
        timestamp = int(time.time()*1e9)
        try:
            data = self.i2c_bus.read_i2c_block_data(SHT_ADDR, 0,6)
        except Exception, e:
            return 0,0,0
        temp = ((( data[0] * 256.0 + data[1]) * 175 ) / 65535.0) - 45
        humid = ((( data[3] * 256.0 + data[4]) * 100 ) / 65535.0)
        # print "T = %6.2f   RH = %6.2f %%" % (temp,humid)
        return temp,humid,timestamp

if __name__=='__main__':
    sht30 = Sht30()
    sht30.enable_periodic_measurement()
    time.sleep(1)
    t,h,ts = sht30.read_periodic()
    print "%d: %.2f %.2f" % (ts,t,h)
    time.sleep(0.3)
    t,h,ts = sht30.read_periodic()
    print "%d: %.2f %.2f" % (ts,t,h)
    time.sleep(0.3)
    t,h,ts = sht30.read_periodic()
    print "%d: %.2f %.2f" % (ts,t,h)

