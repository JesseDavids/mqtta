#!/usr/bin/env python3
#mqtta version 1
from icmplib import ping
import os
import logging
import socket
import paho.mqtt.client as mqtt
import time
import subprocess
import threading
import psutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
p_p = os.getcwd()
file_handler = logging.FileHandler(p_p + "/mqtta.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


while True:

    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 80))
    ip = s.getsockname()[0]
    s.close()  

    broker = "192.168.124.147"
    client = mqtt.Client(ip)
    client.connect(broker)
    client.subscribe("workstation/{}/w/ping".format(ip), 2)


    def on_message(client, userdata, message):

        m = str(message.payload.decode("utf-8"))
        topic = message.topic

        ip2 = ""
        count2 = ""
        interval2 = ""

        ip2, count2, interval2 = m.split(' ')
        
        host = ping(str('{}'.format(ip2)), count = int(count2), interval = float(interval2), privileged=False)
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

        #if(topic == "workstation/{}/w/ping".format(ip)):            
        client.publish("workstation/{}/n/ping".format(ip), str(IPstats), 2, False)
        #logger.info(str(IPstats))

    client.on_message = on_message
    client.loop_start()
    time.sleep(14)
    client.disconnect()

quit()