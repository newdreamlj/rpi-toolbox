#!/usr/bin/env python
#
# 2017-4-19 by NewDream
#
# i2c interaction with SHT30


import time
import paho.mqtt.client as mqtt
import threading
import uuid
import os
import sys
import sht30.i2c as SHT30
import adxl345.i2c as ADXL
import logging
import RPi.GPIO as GPIO
import argparse

MQTT_PUBLISH_PERIOD = 2
global timer_publish_triggered
timer_publish_triggered = 0
global server_connected
server_connected = 0


def on_connect(client, userdata, rc):
    result = {
        0: "Connection successful",
        1: "Connection refused - incorrect protocol version",
        2: "Connection refused - invalid client identifier ",
        3: "Connection refused - server unavailable ",
        4: "Connection refused - bad username or password ",
        5: "Connection refused - not authorised "
    }
    if rc == 0:
        logging.info(result[rc])
        global server_connected
        server_connected = 1
        # print result[rc]
    else:
        logging.warning(result[rc])

def on_disconnect(client, obj, rc):
    logging.warning("Disconnected...")
    global server_connected
    server_connected = 0
    # client.reconnect()

def timer_publish_trigger():
    # print "triggered"
    threading.Timer(MQTT_PUBLISH_PERIOD, timer_publish_trigger).start()
    global timer_publish_triggered
    timer_publish_triggered = 1

def sensor_loop():
    global timer_publish_triggered
    global server_connected
    timer_publish_trigger()
    COUNT_PER_1S = 1
    count_for_1s = 0
    # adxl.flash_fifo()
    print "sending %d" % server_connected
    while server_connected == 1:
        if timer_publish_triggered == 1:
            timer_publish_triggered = 0
            count_for_1s = count_for_1s + 1
            # every 1.0 s
            if count_for_1s >= COUNT_PER_1S:
                count_for_1s = 0
                # upload sht             
                try:
                    temp,humid,timestamp = sht30.read_periodic()
                    # print (temp,humid,timestamp)
                    if timestamp !=0:
                        payload = '{"mac":"%s","ts":%d,"c_temp":%.2f,"c_humid":%.2f}' % (mac,timestamp,temp,humid);
                        client.publish("tddt/rpi/rpi-001/s_temp_humid",payload)
                        # print payload
                    else:
                        logging.error("no sht3x data")
                except Exception, e:
                    print e
                    logging.error(e)

                # upload human detection
                try:
                    human_detected = GPIO.input(12)
                    timestamp = int(time.time()*1e9)
                    payload = '{"mac":"%s","ts":%d,"c_human_detected":%d}' % (mac,timestamp,human_detected);
                    client.publish("tddt/rpi/rpi-001/s_human",payload)
                except Exception, e:
                    print e
                    logging.error(e)

            # every X0.1sX 1.0 s
            #try:
            #    ax,ay,az,timestamp = adxl.read()
            #    if timestamp != 0:
            #        payload = '{"mac":"%s","ts":%d,"c_ax":%.3f,"c_ay":%.3f,"c_az":%.3f}' % (mac,timestamp,ax,ay,az);
            #        client.publish("tddt/rpi/rpi-001/s_acceleration",payload)
            #        print payload
            #except Exception, e:
            #    print e
            #    logging.error(e)
        else:
            time.sleep(0.001)


if __name__ == "__main__":
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default="localhost")
    parser.add_argument('--port', type=int, default=1883)
    parser.add_argument('--username', type=str, default=None)
    parser.add_argument('--password', type=str, default=None)
    args = parser.parse_args()

    logging.basicConfig(filename='sensorPi_internal.log',level=logging.DEBUG,format='%(asctime)s  %(message)s')
    
    logging.info(args)

    sht30 = SHT30.Sht30()
    sht30.enable_periodic_measurement()
    # adxl = ADXL.Adxl345()
    # adxl.init()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12,GPIO.IN)

    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    logging.info("MAC:"+ mac)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    if args.username != None:
        client.username_pw_set(args.username, args.password)
    client.loop_start()

    # if len(sys.argv) > 1:
    #     interface = sys.argv[1]
    # else:
    #     interface = 'wlan0'   
    # wifi_scan_result = [[cell.signal, cell.ssid, cell.address] for cell in Cell.all(interface)] 
    # countdown_1min=2

    while 1:
        try:
            print "try connecting..."
            logging.info("Try connecting to server...")
            client.connect(args.host, args.port, 10)            
            # client.loop_start()
            time.sleep(2)
            sensor_loop()
        except Exception,e:
            print e
            logging.error(e)
            # client.reinitialise()
        time.sleep(2)

