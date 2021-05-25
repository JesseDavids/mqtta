#!/usr/bin/env python3
#mqtta version 1

#end-of-life plugin
#get eol from file and retrieve it and display it

from io import StringIO
import utility as utility
from datetime import datetime
import time
from core import MyApp
import os
import paho.mqtt.client as mqtt

class Plugin:
    def process(self):
        f = utility.Utility()
        ip = f.ip()
        eol = f.eol()
        hostname = f.host()
        #variable extracted from topic name
        subT = f.subtopic()
        #broker ip set in setup.config file
        BROKER = f.broker()
        DV = f.DynamicVariable()
        
        while True:
            broker = BROKER
            client = mqtt.Client(ip)
            client.connect(broker)
            client.loop_start()
            if(subT == ""):
                
                client.publish(f"workstation/{hostname}/n/eol", str(eol), 2, False)

            setattr(f, "logText", str(eol))
            f.log()
            time.sleep(0.5)
            client.disconnect()
            exit()
