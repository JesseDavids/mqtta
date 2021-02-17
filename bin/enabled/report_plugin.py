#!/usr/bin/env python3
#mqtta version 1
import logging
import os
import socket
import time
import paho.mqtt.client as mqtt
import subprocess
import psutil
import json

#logging to a file (file_handler)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
p_p = os.getcwd()
file_handler = logging.FileHandler(p_p + "/mqtta.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


while True:

	#getting ip addr of host pc
	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("1.1.1.1", 80))
	ip = s.getsockname()[0]
	s.close()

	#get current hostname
	hostname = socket.gethostname()

	#get current cpu usage
	cpu_usage = str(psutil.cpu_percent()) + " %"

	#get current memory usage
	ram_usage = str(psutil.virtual_memory().percent) + " %"

		#get percentage of used disk space on file system
	hdd = psutil.disk_usage('/')
	total = (hdd.total / (2**30))
	used = (hdd.used / (2**30))

	format_total = '{0:.3g}'.format(total)
	format_used = '{0:.3g}'.format(used)

		#used/total
	storage_used_total = str(format_used) + " GB" + " / " + str(format_total) + " GB"
		#used percentage
	used_percentage = float(format_used) / float(format_total) * 100
	used_percentage2 = '{0:.3g}'.format(used_percentage)

	#print(system_uptime)
	uptime = (float)(subprocess.check_output(['cat', '/proc/uptime']).decode('utf-8').split()[0])
	sec = uptime
	ty_res = time.gmtime(sec)
	res = time.strftime("%H:%M:%S", ty_res)

	#system info
	system = {}
	system['system info'] = []
	system['system info'].append({
		'Hostname': hostname,
		'IP': ip,
		'CPU usage': cpu_usage,
		'MEM usage': ram_usage,
		'Storage': storage_used_total,
		'Used %': used_percentage2,
		'SystemUptime': res})


	broker = "192.168.124.147"
	client = mqtt.Client(ip)
	client.connect(broker)
	client.subscribe("workstation/{}/r/report".format(ip), 2)


	def on_message(client, userdata, message):
		
		m = str(message.payload.decode("utf-8"))
		topic = message.topic

		if(topic == "workstation/{}/r/report".format(ip)):
			client.publish("workstation/{}/n/report".format(ip), str(system) , 2, False)
			logger.info(str(system))			
		
	client.on_message = on_message

	client.loop_start()
	time.sleep(0.5)
	client.disconnect()

quit()