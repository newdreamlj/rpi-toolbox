#!/usr/bin/env python
#
# 2017-4-19 by NewDream
#
# i2c interaction with SHT30


import time
import i2c.voc as VOC
import i2c.sht30 as SHT30
import uart.pm25 as PM25
import uart.co2 as CO2

def sensor_loop():
    status , tvoc = VOC.tvoc_read()
    # print "tvoc = %d" % tvoc

    temp, humid = SHT30.sht_read()
    # print "T = %.2f, H = %.2f%%" % (temp,humid)

    serial = PM25.pm25_init()
    pm25 = PM25.pm25_read(serial)
    # print "PM2.5 = %d" % pm25
    PM25.pm25_close(serial)

    serial = CO2.co2_init()
    co2 = CO2.co2_read(serial)
    # print "CO2 = %d" % co2
    CO2.co2_close(serial)

    print "tvoc=%d T=%.2f H=%.2f%% PM2.5=%d CO2=%d" % (tvoc,temp,humid,pm25,co2)

if __name__ == "__main__":

    while 1:
	try:
            sensor_loop()
	except Exception,e:
            print e
            # client.reinitialise()
        time.sleep(1.1)

