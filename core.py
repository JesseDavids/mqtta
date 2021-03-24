#!/usr/bin/env python3
import importlib
import os
import paho.mqtt.client as mqtt
import utility as utility
import time
##Main Class
class MyApp:
    _plugins = []
    # we are going to receive a list of plugins, messages and topics as parameters
    def __init__(self, plugins:list=[], msg=str, tpc=str):
        self.msg = msg
        self.tpc = tpc
        
        Version = 1
        dirname = os.path.dirname(__file__)
        #get current working directory
        p_p = os.getcwd()
        #list all items in the directory
        plug_file = os.listdir(p_p)
        #create a list of plugs
        plug = []

        for f in plug_file:
            if f.endswith("_plugin.py"):
                #append all plugins to the list
                plug.append(f)
                
        for x in plug:
            #x is going to be the plugin, so its the file path + plugin name then open it
            filepath = p_p+"/"+x
            filehandle = open(filepath, 'r')            
            while True:                    
                line = filehandle.readline()
                line = filehandle.readline()
                for x in (plug):
                    #if these conditions are met in the plugin file it may proceed
                    #it gets the extention .py chopped off and appended to a new list
                    if "#!/usr/bin/env python3" and "#mqtta version {}".format(Version) in line:
                        for m in plug:
                            m = "{}".format(x[0:-3])
                            if m.endswith("_plugin"):
                                #plugins = []
                                plugins.append(m)
                                
                            break
                    #if the plugins is not empty, create a new list with initialised objects with classes .Plugin()
                    #to the self variable (self._plugins)
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
        #This is our main function called run and im instantiating objects from the utility file
        f = utility.Utility()
        ip = f.ip()
        hostname = f.host()
        BROKER = f.broker()
        
        while True:
            #set the function up for mqtt communication and set subscription
            broker = BROKER
            #i used the ip address to make it unique, you can add anything you want but it must be unique
            client = mqtt.Client(ip)
            #connect client to broker
            client.connect(broker)
            #set subscribtion
            client.subscribe("#", 2)
            #start the loop
            client.loop_start()
            #the on_message function comes from the paho library and waits for any incoming
            #messages from said subscribe topic
            def on_message(client, userdata, message):
                m = str(message.payload.decode("utf-8"))
                topic = message.topic

                #exmaple topics:
                #workstation/192.168.0.1/r/report_plugin/  
                #device/username/w/ping_plugin/  and the message -m "IP / Count / Interval
                #Each plugin has its own instructions

                #When creating plugins it should qualify by having the shabang, version and "_plugin.py" extention
                #Note: Version should match the core version

                lastWord = topic.split("/")[-1]
                MyApp.run.lastWord = lastWord
                
                N = 2
                secondWord = topic.split("/")[N-1]
                
                if (secondWord == hostname or secondWord == ip or secondWord == "list"):
                    #when using list_plugin
                    #example: (workstations/list_plugin/)
                    #it will list all devices connected to the broker you set in Config file
                    
                    MyApp.run.m2 = topic.split("/")[-2]

                    m1 = m
                    MyApp.run.DynamicVar = m1

                    self.msg = MyApp.run.m2

                    someVar = self.msg + "_plugin"
                    
                    
                    for plugin in self._plugins:
                        p = str(plugin)
                        p2 = p.split(".")[0]
                        p3 = (p2[1:])
                        
                        
                        if p3 == someVar:
                            plugin.process()
            
            #attach the function to the client
            client.on_message = on_message
            #you can set this to your liking, for active listening i suggest 0.5 seconds
            time.sleep(0.5)
            #then disconnect
            client.disconnect()