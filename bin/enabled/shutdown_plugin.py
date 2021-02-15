#!/usr/bin/env python3
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

#logging to a file (file_handler)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('/var/log/mqtta.log')
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
    client.subscribe("workstation/{}/r/shutdown".format(ip), 2)

    def on_message(client, userdata, message):
        m = str(message.payload.decode("utf-8"))
        topic = message.topic

        if(topic == "workstation/{}/r/shutdown".format(ip)):
            client.publish("workstation/{}/n/shutdown".format(ip), jsonOK, 2, False)
            logger.info("System shutdown..")
            time.sleep(2)
            os.system("shutdown -h now")

    client.on_message = on_message
    client.loop_start()
    time.sleep(0.5)
    client.disconnect()

quit()






