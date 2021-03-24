#!/usr/bin/env python3
#mqtta version 1
import subprocess
import utility as utility
import time
import paho.mqtt.client as mqtt
from io import StringIO


Traceroute_Help = (
    "\nGUIDANCE I SHALL GIVE"
    "\n"
    "\nThis plugin will make a traceroute to desired IP or website name"
    "\n"
    "\nTopic = workstation/hostname-or-ip/parameter/traceroute/"
    "\nrequires a message parameter "
    "\nMessage = 1.1.1.1 , or www.google.com "
)
class Plugin:
    def process(self):
        f = utility.Utility()
        ip = f.ip()
        hostname = f.host()
        BROKER = f.broker()
        subT = f.subtopic()

        DV = f.DynamicVariable()
        while True:
            broker = BROKER
            client = mqtt.Client(ip)    
            client.connect(broker)
            client.loop_start()
            if(subT == "help"):
                client.publish(f"workstation/{hostname}/n/traceroute/help", str(Traceroute_Help), 2, False)
            elif(subT == ""):
                traceroute_result = subprocess.run(['traceroute', f'{DV}'], stdout=subprocess.PIPE)
                rt = traceroute_result.stdout.decode('utf-8')   
                client.publish(f"workstation/{hostname}/n/traceroute", str(rt), 2, False)
                setattr(f, 'logText', str(rt))
                f.log()

            break
            time.sleep(0.5)
            client.disconnect()
            quit()
