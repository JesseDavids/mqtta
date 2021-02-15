#!/usr/bin/env python3
import logging
import os
import socket
import time
import paho.mqtt.client as mqtt
import subprocess
import psutil
import json
import importlib
from multiprocessing import Process

Version = 1

path = ""
dirname = os.path.dirname(__file__)
plugin_path = "/home/dankninja/Documents/mqtta-project/plugin/bin/enabled"
#filename = os.path.join(dirname, plugin_path)
plugin_file = os.listdir(plugin_path)
plugin_list = []

for f in plugin_file:
	if f.endswith("_plugin.py"):
		plugin_list.append(f)
		#print(plugin_list)

for x in plugin_list:
	filepath = plugin_path+"/"+x
	filehandle = open(filepath, 'r')
	while True:
		line = filehandle.readline()
		line = filehandle.readline()
		for x in (plugin_list):
			
			if "#!/usr/bin/env python3" and "#mqtta version {}".format(Version) in line:
				for m in plugin_list:
					m = "{}".format(x[0:-3])
										
					if m.endswith("_plugin"):
						module_list = []
						module_list.append('enabled.'+m)
						
						def func1():
							while True:
								str1 = " ".join(module_list)
								print(str1)
								globals()[str1] = importlib.import_module(str1)
								
								time.sleep(1)

						if __name__ == '__main__':
							proc1 = Process(target = func1)
							proc1.start()
						break;
			else:
				#print("{}".format(x) + " not found")            
				break;
	quit()


filehandle.close()