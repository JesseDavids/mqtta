#!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
from core import MyApp
import paho.mqtt.client as mqtt


class Plugin:
    
    def process(self):

        f = utility.Utility()
        system = f.system()
        ip = f.ip()

        #topic = f"workstation/{ip}/n/report"

        while True:    
            broker = "192.168.124.147"
            ip = f.ip()
            client = mqtt.Client(ip)
            client.connect(broker)
            #client.subscribe(f"workstation/{ip}/r/report", 2, )
            client.loop_start()

            client.publish(f"workstation/{ip}/n/report", str(system), 2, False)
            setattr(f, "logText", str(system))
            f.log()
            #client.loop_start()
            time.sleep(0.5)
            client.disconnect()
            quit()