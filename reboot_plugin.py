#!/usr/bin/env python3
#mqtta version 1
import utility as utility
import time
import paho.mqtt.client as mqtt
import os

Reboot_Help = (
    "\nGUIDANCE I SHALL GIVE"
    "\n"
    "\nThis plugin will reboot any target PC"
    "\n"
    "\nTopic = workstation/hostname-or-ip/parameter/reboot/  <--- plugin does not require a message parameter"
)
class Plugin:

	def process(self):

		f = utility.Utility()
		#while True:
		ip = f.ip()
		hostname = f.host()
		BROKER = f.broker()
		subT = f.subtopic()
		while True:
			broker = BROKER
			client = mqtt.Client(ip)
			client.connect(broker)
			client.loop_start()
			if(subT == "help"):
				client.publish(f"workstation/{hostname}/n/reboot/help", str(Reboot_Help), 2, False)
				quit()
			elif(subT == ""):
				client.publish(f"workstation/{hostname}/n/reboot", f"Rebooting system {hostname}", 2, False)
				setattr(f, "logText", "Rebooting System...")
				f.log()
				time.sleep(2)
				os.system("reboot")
				time.sleep(0.5)
				client.disconnect()
				quit()

