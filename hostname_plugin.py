##!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
import paho.mqtt.client as mqtt
import os

"""
topic = (workstation/pc1/w/hostname/)
message = new hostname (pc2)
"""
Hostname_Help = (
    "\nGUIDANCE I SHALL GIVE"
    "\n"
    "\nThis plugin will ping any target PC, with count and interval or default"
    "\n"
    "\nTopic = workstation/hostname-or-ip/parameter/hostname/  <--- plugin requires a message parameter"
    "\ni.e Message = newPC1"
    
)
class Plugin:

    def process(self):
        f = utility.Utility()
        ip = f.ip()
        hostname = f.host()
        BROKER = f.broker()
        DV = f.DynamicVariable()
        subT = f.subtopic()
        
        while True:
                
            broker = BROKER
            client = mqtt.Client(ip)
            client.connect(broker)
            client.loop_start()
            if(subT == "help"):
                client.publish(f"workstation/{hostname}/n/setting/hostname/help", str(Hostname_Help), 2, False)
                quit()
            elif(subT == ""):
                os.system(f"hostnamectl set-hostname {DV} --static")
                client.publish(f"workstation/{hostname}/n/hostname", f"Hostname changed successfully to {DV} ", 2, False)
                setattr(f,"logText", f"Hostname changed to, {hostname}")
                f.log()
                break
                time.sleep(0.5)
                client.disconnect()
                quit()