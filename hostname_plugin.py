##!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
import paho.mqtt.client as mqtt
import os

class Plugin:

    def process(self):
                
        f = utility.Utility()
        #while True:
        ip = f.ip()
        hostname = f.changehostname()

        while True:
                
            broker = "192.168.124.147"
            client = mqtt.Client(ip)
            client.connect(broker)
            client.loop_start()
            
            os.system(f"hostnamectl set-hostname {hostname} --static")
            client.publish(f"workstation/{ip}/n/setting/hostname_new", f"Hostname changed successfully to {hostname} ", 2, False)
            setattr(f,"logText", f"Hostname changed to, {hostname}")
            f.log()

            time.sleep(0.5)
            client.disconnect()
            quit()