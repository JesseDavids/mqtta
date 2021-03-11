import importlib
import os
import paho.mqtt.client as mqtt
import utility as utility
import time

class MyApp:

    _plugins = []
    # we are going to receive a list of plugins as parameter
    def __init__(self, plugins:list=[], msg=str, tpc=str):
        self.msg = msg
        self.tpc = tpc

        Version = 1
        dirname = os.path.dirname(__file__)
        p_p = os.getcwd()
        plug_file = os.listdir(p_p)
        plug = []

        for f in plug_file:
            if f.endswith("_plugin.py"):
                plug.append(f)
                #print(f)
        for x in plug:
            filepath = p_p+"/"+x
            filehandle = open(filepath, 'r')            
            while True:                    
                line = filehandle.readline()
                line = filehandle.readline()
                for x in (plug):
                    if "#!/usr/bin/env python3" and "#mqtta version {}".format(Version) in line:
                        for m in plug:
                            m = "{}".format(x[0:-3])
                            if m.endswith("_plugin"):
                                #plugins = []
                                plugins.append(m)
                                
                            break
                    if plugins != []:
                        #create a list of plugins
                        self._plugins = [
                            #import the module and initialise it at the same time
                            importlib.import_module(plugin,".").Plugin() for plugin in plugins
                        ]
                break
            break
        
        filehandle.close()
        
    def run(self):
        
        f = utility.Utility()
        ip = f.ip()
        hostname = f.host()
        
        while True:
            #print("Starting..")
            broker = "192.168.124.147"
            client = mqtt.Client(ip)
            client.connect(broker)
            client.subscribe("#", 2)
            client.loop_start()
            #the on_message function comes from the paho library
            def on_message(client, userdata, message):
                m = str(message.payload.decode("utf-8"))
                topic = message.topic
                #get second word which will be hostname
                N = 2
                secondWord = topic.split("/")[N-1]
                
                if (secondWord == hostname or secondWord == ip):
                    #variable used to pick plugin                
                    MyApp.run.m2 = topic.split('/')[-1]

                    m1 = m
                    MyApp.run.DynamicVar = m1

                    self.msg = MyApp.run.m2
                    
                    for plugin in self._plugins:
                        p = str(plugin)
                        p2 = p.split(".")[0]
                        p3 = (p2[1:])
                        #print(p3)
                    
                        if p3 == self.msg:
                            plugin.process()

            client.on_message = on_message
            #client.loop_start()
            time.sleep(0.5)
            client.disconnect()