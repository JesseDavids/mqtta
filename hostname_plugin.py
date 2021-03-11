##!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
import paho.mqtt.client as mqtt
import os
class Plugin:

    def process(self):
        f = utility.Utility()
        ip = f.ip()
        hostname = f.host()
        DV = f.DynamicVariable()
        while True:
                
            broker = "192.168.124.147"
            client = mqtt.Client(ip)
            client.connect(broker)
            client.loop_start()
            os.system(f"hostnamectl set-hostname {DV} --static")
            client.publish(f"workstation/{hostname}/n/setting/hostname_new", f"Hostname changed successfully to {hostname} ", 2, False)
            setattr(f,"logText", f"Hostname changed to, {hostname}")
            f.log()
            break
            time.sleep(0.5)
            client.disconnect()
            quit()