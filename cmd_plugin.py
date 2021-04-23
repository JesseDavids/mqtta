#!/usr/bin/env python3
#mqtta version 1)

import subprocess
from io import StringIO
import utility as utility
from datetime import datetime
import time
from core import MyApp
import os
import paho.mqtt.client as mqtt

"""
topic = workstation/pc/r/report/
message = ""
"""

class Plugin:
    
    def process(self):
        #instantiate the utility file
        f = utility.Utility()
        ip = f.ip()
        hostname = f.host()
        #variable extracted from topic name
        subT = f.subtopic()
        #broker ip set in setup.config file
        BROKER = f.broker()
        DV = f.DynamicVariable()

        while True:
            #set broker address    
            broker = BROKER
            #set client, should be unique
            client = mqtt.Client(ip)
            #connect to broker
            client.connect(broker)
            #begin client loop
            client.loop_start()
            #publish information to sub-topic
            title = "Message"

            #getting the date and time
            date = datetime.now()
            dt_string = date.strftime("%d/%m/%Y %H:%M")

            #command = f"zenity --info --title={title} --text='Sent from {sender} on {dt_string}\n\nMessage: {DV}' --width=300 --height=150"
            #icon = "/home/ninja/Documents/Work/mqtta/bell_ring_outline_icon_139893.ico"
            if(subT == ""):
                #message1 = DV.split("/")[-1]
                #sender1 = DV.split("/")[0]

                #os.system(f"Command=$(zenity --info --window-icon={icon} --title={title} --text='Sent from {sender} on {dt_string}\n\nMessage: {DV}' --width=300 --height=150); echo $Command")
            
                msg_result = subprocess.run([DV], stdout=subprocess.PIPE, shell=True)
                rt = msg_result.stdout.decode('utf-8')
                #os.system(f"{DV}")
                #r = subprocess.check_output([DV], shell=True)
                
                
                client.publish(f"workstation/{hostname}/n/message", str(rt), 2, False)
                #set log file contents
                #setattr(f, "logText", f"from {sender1} message: {message1} at {dt_string}")
                #f.log()
                #sleep for 0.5 seconds
                time.sleep(0.5)
                #disconnect client
                client.disconnect()
                #quit loop
                exit()