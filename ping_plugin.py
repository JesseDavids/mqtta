#!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
import paho.mqtt.client as mqtt
from icmplib import ping
import multiprocessing


class Plugin:

    def process(self):

        f = utility.Utility()
        ip = f.ip()
        #set ping rate in utilities file in the ping object

        pingRate = f.ping()
        print(pingRate)


        while True:
            broker = "192.168.124.147"
            client = mqtt.Client(ip)
            client.connect(broker)
            #client.subscribe(f"workstation/{ip}/w/ping", 2)
            client.loop_start()

        
            #below value will be set in the settings file
            #setattr(f, "ping_ip", "")
            ip2 = "1.1.1.1"
            count2 = "4"
            interval2 = "0.5"
            
            #IP / COUNT / INTERVAL 
            #1.1.1.1 30 0.2
            if (pingRate == "default"):
                host = ping(str(f'{ip2}'), count = int(count2), interval = float(interval2), privileged=False)
            else:
                ip2, count2, interval2 = pingRate.split(' ')
            host = ping(str(f'{ip2}'), count=int(count2), interval=float(interval2), privileged=False)
            
            IPstats = {}
            IPstats['IP Stats'] = []
            IPstats['IP Stats'].append({
                'MIN': host.min_rtt,
                'MAX': host.max_rtt,
                'AVG': host.avg_rtt,
                'Packets Sent': host.packets_sent,
                'Packets Received': host.packets_received,
                'Packet Loss': host.packet_loss    
            })

            client.publish(f"workstation/{ip}/n/ping", str(IPstats), 2, False)
            setattr(f, "logText", str(IPstats))
            f.log()
            break
            time.sleep(10)
            client.disconnect()
            quit()