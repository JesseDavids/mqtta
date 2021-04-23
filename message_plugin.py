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

        Message_Help = (
            "\nHOW TO USE THE MESSAGING PLUGIN"
            "\n"
            "\nThis plugin will send a message to target PC"
            "\n"
            "\nExample Topic: workstation/hostname or ip/parameter/message/"
            "\nExample message: Your Name / Message"
            "\n"
            "\nJohn Doe / We have a meeting at 10AM. Don't be late."
            "\n"
            "\nMary / Hi John, need you to work over time tomorrow."
        )
        

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

            if(subT == "help"):
                client.publish(f"workstation/{hostname}/n/message/help", str(Message_Help), 2, False)

            if(subT == ""):
                message1 = DV.split("/")[-1]
                sender1 = DV.split("/")[0]

                #os.system(f"Command=$(zenity --info --window-icon={icon} --title={title} --text='Sent from {sender} on {dt_string}\n\nMessage: {DV}' --width=300 --height=150); echo $Command")
                cmd = (f"Command=$(zenity --display=$DISPLAY --info --title={title} --text='Sent from {sender1} on {dt_string}\n\nMessage: {message1}' --width=300 --height=150); echo $Command")
                subprocess.check_output([cmd], shell=True)
                
                
                client.publish(f"workstation/{hostname}/n/message", str("Okayy"), 2, False)
                #set log file contents
                setattr(f, "logText", f"from {sender1} message: {message1} at {dt_string}")
                f.log()
                #sleep for 0.5 seconds
                time.sleep(0.5)
                #disconnect client
                client.disconnect()
                #quit loop
                exit()