#!/usr/bin/python3
##create a running loop
import logging
import os
import netifaces as ni
import socket
import time
import datetime
import paho.mqtt.client as mqtt
#getting system info
import psutil
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('/var/log/testmqtt.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

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

#get percentage of free disk space on file system
hdd = psutil.disk_usage('/')
total = (hdd.total / (2**30))
used = (hdd.used / (2**30))
free = (hdd.free / (2**30))

format_total = '{0:.3g}'.format(total)
format_used = '{0:.3g}'.format(used)
format_free = '{0:.3g}'.format(free)
#used/total
storage_used_total = str(format_used) + " GB" + " / " + str(format_total) + " GB"
#storage_free = str(format_free) + " GB" 

#used percentage
used_percentage = float(format_used) / float(format_total) * 100
used_percentage2 = '{0:.3g}'.format(used_percentage)

#system info
system = {}
system['system info'] = []
system['system info'].append({
	'Hostname': hostname,
	'IP': ip,
	'CPU usage': cpu_usage,
	'MEM usage': ram_usage,
	'Storage': storage_used_total,
	'Used %': used_percentage2})


#print("{}".format(system))

#logging ip addr
logger.info("Running on ip: {}...".format(ip))
#some json to send with notice
somejson = '{"Result": "OK"}'


while True:

	def on_message(client, userdata, message):
		print("message: ",str(message.payload.decode("utf-8")))
		print("topic: ",message.topic)


#Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport=tcp)
	broker="192.168.124.147"

	#creating a new instance (ip = this must be unique)
	client = mqtt.Client(ip)
	client.connect(broker)
	client.subscribe([("workstation/{}/r/report".format(ip),2),("workstation/{}/w/setting/hostname_new".format(ip),2), ("workstation/test/{}".format(ip),2), ("workstation/{}/w/shutdown".format(ip),2), ("workstation/{}/w/reboot".format(ip),2)])


	def on_message(client, userdata, message):
		m = str(message.payload.decode("utf-8"))
		print("message received ", str(message.payload.decode("utf-8")))
		print("message topic= ", message.topic)
		topic = message.topic
		#just a test topic to ensure proper connection
		if(topic == "workstation/test/{}".format(ip)):
			logger.info("Test succesfull")
			client.publish("workstation/test/{}".format(ip), "Test Successful", 2, False)

		elif(topic == "workstation/{}/w/setting/hostname_new".format(ip)):
			client.publish("workstation/{}/n/setting/hostname_new".format(ip), somejson, 2, False)
			os.system("hostnamectl set-hostname {} --static".format(m))
			logger.info("Hostname changed successfully to {} ".format(m))

		elif(topic == "workstation/{}/w/shutdown".format(ip)):
			client.publish("workstation/{}/n/shutdown".format(ip), somejson, 2, False)
			logger.info("System shutdown..")
			time.sleep(2)
			os.system("shutdown -h now")

		elif(topic == "workstation/{}/w/reboot".format(ip)):
			client.publish("workstation/{}/n/reboot".format(ip), somejson, 2, False)
			logger.info("System is rebooting..")
			time.sleep(2)
			os.system("reboot")

		elif(topic == "workstation/{}/r/report".format(ip)):
			client.publish("workstation/{}/n/report".format(ip), str(system) , 2, False)
			logger.info(str(system))


	client.on_message = on_message

	client.loop_start()
	time.sleep(0.5)
	client.disconnect()

quit()
