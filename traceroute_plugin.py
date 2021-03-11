#!/usr/bin/env python3
#mqtta version 1
import subprocess
import utility as utility
import time
import paho.mqtt.client as mqtt
from io import StringIO
"""
This plugin requires you to 'sudo apt install traceroute', currently just working on LINUX
------------------------------
HOW TO USE THE PLUGIN ->
command: f"traceroute {address}"
i.e: "traceroute 192.168.0.1"
------------------------------
"""
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
            traceroute_result = subprocess.run([f'traceroute', '{DV}'], stdout=subprocess.PIPE)
            rt = traceroute_result.stdout.decode('utf-8')   
            client.publish(f"workstation/{hostname}/n/traceroute", str(rt), 2, False)
            setattr(f, 'logText', str(rt))
            f.log()
            break
            time.sleep(0.5)
            client.disconnect()
            quit()
