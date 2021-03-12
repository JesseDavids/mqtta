#!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
import paho.mqtt.client as mqtt
import os
class Plugin:

	def process(self):

		f = utility.Utility()
		#while True:
		ip = f.ip()
		hostname = f.host()
		BROKER = f.broker()
		while True:
			broker = BROKER
			client = mqtt.Client(ip)
			client.connect(broker)
			client.loop_start()
			client.publish(f"workstation/{hostname}/n/reboot", "Rebooting system", 2, False)
			setattr(f, "logText", "Rebooting System...")
			f.log()
			time.sleep(2)
			os.system("reboot")
			time.sleep(0.5)
			client.disconnect()
			quit()

