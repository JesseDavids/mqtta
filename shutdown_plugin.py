#!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
import os
import paho.mqtt.client as mqtt

class Plugin:
    def process(self):
                
        f = utility.Utility()
        ip = f.ip()

        while True:
            
            broker = "192.168.124.147"
            client = mqtt.Client(ip)
            client.connect(broker)
            client.loop_start()
            client.publish(f"workstation/{ip}/n/shutdown", "shutting down", 2, False)
            setattr(f, "logText", f"Shutting down pc {ip}")
            time.sleep(2)
            f.log()
            os.system("shutdown -h now")
            time.sleep(0.5)
            client.disconnect()
            quit()
