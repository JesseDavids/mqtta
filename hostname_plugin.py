##!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
import paho.mqtt.client as mqtt
import os

"""
topic = (workstation/pc1/w/hostname_plugin/)
message = new hostname (pc2)
"""
class Plugin:

    def process(self):
        f = utility.Utility()
        ip = f.ip()
        hostname = f.host()
        BROKER = f.broker()
        DV = f.DynamicVariable()
        while True:
                
            broker = BROKER
            client = mqtt.Client(ip)
            client.connect(broker)
            client.loop_start()
            os.system(f"hostnamectl set-hostname {DV} --static")
            client.publish(f"workstation/{hostname}/n/setting/hostname_new", f"Hostname changed successfully to {DV} ", 2, False)
            setattr(f,"logText", f"Hostname changed to, {hostname}")
            f.log()
            break
            time.sleep(0.5)
            client.disconnect()
            quit()