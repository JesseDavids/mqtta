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
i.e (workstation/pc1/w/traceroute/)
message = IP or web name to traceroute such as www.google.com
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
            traceroute_result = subprocess.run(['traceroute', f'{DV}'], stdout=subprocess.PIPE)
            rt = traceroute_result.stdout.decode('utf-8')   
            client.publish(f"workstation/{hostname}/n/traceroute", str(rt), 2, False)
            setattr(f, 'logText', str(rt))
            f.log()
            break
            time.sleep(0.5)
            client.disconnect()
            quit()
