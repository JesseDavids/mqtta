#!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
from core import MyApp
import paho.mqtt.client as mqtt

"""
topic = workstation/pc/r/report/   <-------- this retrieves all below information in one json string
topic = workstation/pc/r/report/ip
topic = workstation/pc/r/report/memory
topic = workstation/pc/r/report/hostname
topic = workstation/pc/r/report/storage
topic = workstation/pc/r/report/uptime
topic = workstation/pc/r/report/cpu
topic = workstation/pc/r/report/help
message = ""
"""
class Plugin:
    
    def process(self):
        #instantiate the utility file
        f = utility.Utility()
        #get system information
        system = f.system()
        #system individual parts
        ip = f.ip()
        memory = f.ram()
        storage = f.storage()
        uptime = f.uptime()
        cpu = f.cpu()
        hostname = f.host()
        
        
        string_of_report_objects = ("-ip\n-memory\n-storage\n-uptime\n-cpu\n-hostname")
        #variable extracted from topic name
        subT = f.subtopic()
        #broker ip set in setup.config file
        BROKER = f.broker()

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
            if(subT == "ip"):
                client.publish(f"workstation/{hostname}/n/report/ip", str(ip), 2, False)

            elif(subT == "memory"):
                client.publish(f"workstation/{hostname}/n/report/memory", str(memory), 2, False)

            elif(subT == "storage"):
                client.publish(f"workstation/{hostname}/n/report/storage", str(storage), 2, False)

            elif(subT == "uptime"):
                client.publish(f"workstation/{hostname}/n/report/uptime", str(uptime), 2, False)

            elif(subT == "cpu"):
                client.publish(f"workstation/{hostname}/n/report/cpu", str(cpu), 2, False)

            elif(subT == "hostname"):
                client.publish(f"workstation/{hostname}/n/report/hostname", str(hostname), 2, False)

            elif(subT == ""):
                client.publish(f"workstation/{hostname}/n/report/system", str(system), 2, False)
            
            elif(subT == "help"):
                client.publish(f"workstation/{hostname}/n/report/help", str(string_of_report_objects), 2, False)
            #set log file contents
            setattr(f, "logText", str(system))
            f.log()
            #sleep for 0.5 seconds
            time.sleep(0.5)
            #disconnect client
            client.disconnect()
            #quit loop
            quit()