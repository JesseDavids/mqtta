#!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
import json
import paho.mqtt.client as mqtt
from icmplib import ping

Ping_Help = (
    "\nGUIDANCE I SHALL GIVE"
    "\n"
    "\nThis plugin will ping any target PC, with count and interval or default"
    "\n"
    "\nTopic = workstation/hostname-or-ip/parameter/ping/  <--- plugin requires a message parameter"
    "\ni.e Message = 1.1.1.1 20 0.2"
    "\nIP = 1.1.1.1 | COUNT = 15 pings | INTERVAL = every 0.2 seconds "
    "\n"
    "\nIf IP, Count and Interval is not specified the plugin will use default values"
    "\nValues = 1.1.1.1 4 0.5"
)
class Plugin:

    def process(self):
        f = utility.Utility()
        ip = f.ip()
        #set ping rate in utilities file in the ping object
        DV = f.DynamicVariable()
        hostname = f.host()
        BROKER = f.broker()
        subT = f.subtopic()
        
        while True:
            broker = BROKER
            client = mqtt.Client(ip)
            client.connect(broker)
            client.loop_start()    
            
            ip2 = "1.1.1.1"
            count2 = "4"
            interval2 = "0.5"

            if(subT == "help" and DV == ""):
                client.publish(f"workstation/{hostname}/n/ping/help", str(Ping_Help), 2, False)
                quit()

            elif(subT == "" and DV == ""):
                host = ping(str(f'{ip2}'), count = int(count2), interval = float(interval2), privileged=False)
                IPstats = {}
                IPstats = {
                    'IP': ip2,
                    'MIN': host.min_rtt,
                    'MAX': host.max_rtt,
                    'AVG': host.avg_rtt,
                    'Packets Sent': host.packets_sent,
                    'Packets Received': host.packets_received,
                    'Packet Loss': host.packet_loss    
                }
                json_IPstats = json.dumps(IPstats, indent=4)
                client.publish(f"workstation/{hostname}/n/ping", str(json_IPstats), 2, False)
                setattr(f, "logText", str(json_IPstats))
                f.log()
                break
                time.sleep(10)
                client.disconnect()
                quit()

            elif(DV != ""):
                ip2, count2, interval2 = DV.split(' ')
                host = ping(str(f'{ip2}'), count=int(count2), interval=float(interval2), privileged=False)            
                IPstats = {}
                IPstats = {
                    'IP': ip2,
                    'MIN': host.min_rtt,
                    'MAX': host.max_rtt,
                    'AVG': host.avg_rtt,
                    'Packets Sent': host.packets_sent,
                    'Packets Received': host.packets_received,
                    'Packet Loss': host.packet_loss    
                }
                json_IPstats = json.dumps(IPstats, indent=4)
                client.publish(f"workstation/{hostname}/n/ping", str(json_IPstats), 2, False)
                setattr(f, "logText", str(json_IPstats))
                f.log()
                break
                time.sleep(10)
                client.disconnect()
                quit()
            
            