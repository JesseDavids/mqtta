#!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
import json
import paho.mqtt.client as mqtt

class Plugin:
    def process(self):
        utilities = utility.Utility()
        ipAddress = utilities.ip()
        DV = utilities.DynamicVariable()
        hostname = utilities.host()
        BROKER = utilities.broker()

        while True:
            broker = BROKER
            client = mqtt.Client(ipAddress)
            client.connect(broker)
            client.loop_start() 

            client.publish("workstation/list", str(hostname + ": " + ipAddress), 2, False)
            
            break
            time.sleep(10)
            client.disconnect()
            quit()