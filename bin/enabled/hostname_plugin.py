##!/usr/bin/env python3
#mqtta version 1
import logging
import os
import netifaces as ni
import socket
import time
import datetime
import paho.mqtt.client as mqtt
import subprocess
import psutil
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
p_p = os.getcwd()
file_handler = logging.FileHandler(p_p + "/mqtta.log")
#print(file_handler)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


jsonOK = '{"Result": "OK"}'

while True:
        
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 80))
    ip = s.getsockname()[0]
    s.close()

    broker = "192.168.124.147"
    client = mqtt.Client(ip)
    client.connect(broker)
    client.subscribe("workstation/{}/w/setting/hostname_new".format(ip), 2)

        
    def on_message(client, userdata, message):
        m = str(message.payload.decode("utf-8"))
        topic = message.topic

        if(topic == "workstation/{}/w/setting/hostname_new".format(ip)):
            #client.publish("workstation/{}/n/setting/hostname_new".format(ip), jsonOK, 2, False)
            os.system("hostnamectl set-hostname {} --static".format(m))
            client.publish("workstation/{}/n/setting/hostname_new".format(ip), "Hostname changed successfully to {} ".format(m), 2, False)
            logger.info("Hostname changed successfully to {} ".format(m))

    client.on_message = on_message

    client.loop_start()
    time.sleep(0.5)
    client.disconnect()

quit()