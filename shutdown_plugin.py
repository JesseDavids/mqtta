#!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
import os
import paho.mqtt.client as mqtt
"""
topic = workstation/pc1/w/shutdown/
message = ""
"""
Shutdown_Help = (
    "\nHOW TO USE THE SHUTDOWN PLUGIN"
    "\n"
    "\nThis plugin will shutdown any target PC"
    "\n"
    "\nTopic = workstation/hostname-or-ip/parameter/shutdown/  <--- plugin does not require a message parameter"
)
class Plugin:
    def process(self):
                
        f = utility.Utility()
        ip = f.ip()
        hostname = f.host()
        BROKER = f.broker()
        subtT = f.subtopic()

        while True:
            
            broker = BROKER
            client = mqtt.Client(ip)
            client.connect(broker)
            client.loop_start()
            if(subtT == "help"):
                client.publish(f"workstation/{hostname}/n/shutdown/help", str(Shutdown_Help), 2, False)
                quit()
            elif(subtT == ""):
                client.publish(f"workstation/{hostname}/n/shutdown", f"shutting down {hostname}", 2, False)
                setattr(f, "logText", f"Shutting down pc {hostname}")
                
                time.sleep(2)
                f.log()
                os.system("shutdown -h now")
                time.sleep(0.5)
                client.disconnect()
                quit()
