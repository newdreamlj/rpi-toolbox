import threading

global timer_publish_triggered
MQTT_PUBLISH_PERIOD = 1.0

def timer_publish_trigger():
    timer_publish_triggered = 1
    print "triggered"
    threading.Timer(MQTT_PUBLISH_PERIOD, timer_publish_trigger)

timer_publish_trigger()

while 1:
    pass
