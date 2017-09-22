#!/usr/bin/env python
#
# 2017-4-19 by NewDream
#
# i2c interaction with SHT30


import smbus
import time
import paho.mqtt.client as mqtt
import uuid
import os
import sys
from wifi import Cell, Scheme
from wifi.utils import print_table, match as fuzzy_match

bus = smbus.SMBus(1)
SHT_ADDR = 0x44
global connected
connected = 0

def on_disconnect(client, obj, rc):
    print "Broker connection failed..."
    # global connected
    # connected = 0
    while 1:
        try:
            client.reconnect()
        except Exception, e:
            continue
        break

def on_connect(client, userdata, rc):
    print "Broker connected!"
    # global connected
    # connected = 1

def sht_read():
    bus.write_i2c_block_data(SHT_ADDR, 0x24, [0x00])
    time.sleep(0.05)
    data = bus.read_i2c_block_data(SHT_ADDR, 0,6)
    temp = ((( data[0] * 256.0 + data[1]) * 175 ) / 65535.0) - 45
    humid = ((( data[3] * 256.0 + data[4]) * 100 ) / 65535.0)
    print "T = %6.2f   RH = %6.2f %%" % (temp,humid)
    return temp,humid

def comp3(x,y):
    if x[0]<y[0]:
        return 1
    else:
        return -1

if __name__ == "__main__":
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    print "MAC:"+ mac

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    print "Try connecting to server..."
    client.connect("www.newdream.xyz", 1883, 10)
    client.loop_start()

    if len(sys.argv) > 1:
        interface = sys.argv[1]
    else:
        interface = 'wlan0'
   
    wifi_scan_result = [[cell.signal, cell.ssid, cell.address] for cell in Cell.all(interface)] 
    countdown_1min=2
    while 1:
        t,h = sht_read()
        try:
            # client.publish("td/room615/temp/1", "%.2f" % t)
            # client.publish("td/room615/humid/1", "%.2f" % h)
            client.publish("td/room615/sensor/1",'{"dev":"RPi","id":"001","mac":"%s","data":{"temp":%.2f,"humid":%.2f}}' % (mac,t,h),retain=True) 
            if countdown_1min == 0:
                countdown_1min=60
                wifi_scan_result = [[cell.signal, cell.ssid, cell.address] for cell in Cell.all(interface)]
                wifi_scan_result.sort(comp3)
                wifi_scan_result = wifi_scan_result[:20]
                print wifi_scan_result
                cell = wifi_scan_result[0]
                b = "%s,%d,%s" %  (cell[2], cell[0], cell[1])
                for cell in wifi_scan_result[1:]:
                    b = b + "|%s,%d,%s" %  (cell[2], cell[0], cell[1])
                client.publish("td/room615/sensor/1/wifi",'{"dev":"RPi","id":"001","mac":"%s","wifi_scan":"%s"}' % (mac,b), retain=True)
        except Exception, e:
            print e
        time.sleep(0.95)
        if countdown_1min>0:
            countdown_1min = countdown_1min - 1


