#!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
from core import MyApp
import paho.mqtt.client as mqtt
class Plugin:
    
    def process(self):
        #instantiate the utility file
        f = utility.Utility()
        #get system information
        system = f.system()
        #get ip address
        ip = f.ip()
        hostname = f.host()

        while True:
            #set broker address    
            broker = "192.168.124.147"
            #set client, should be unique
            client = mqtt.Client(ip)
            #connect to broker
            client.connect(broker)
            #begin client loop
            client.loop_start()
            #publish information to topic
            client.publish(f"workstation/{hostname}/n/report", str(system), 2, False)
            #set log file contents
            setattr(f, "logText", str(system))
            f.log()
            #sleep for 0.5 seconds
            time.sleep(0.5)
            #disconnect client
            client.disconnect()
            #quit loop
            quit()