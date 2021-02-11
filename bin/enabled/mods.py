#!/usr/bin/env python3

import os

path = ""
dirname = os.path.dirname(__file__)
plugin_path = "/home/dankninja/Documents/mqtta-project/plugin/bin/enabled"
#filename = os.path.join(dirname, plugin_path)
plugin_file = os.listdir(plugin_path)
plugin_list = []

for f in plugin_file:
    if f.endswith(".plugin"):
        plugin_list.append(f)
        


for x in (plugin_list):
    #print(x)
    filepath = plugin_path+"/"+x
    #print(filepath)
    filehandle = open(filepath, 'r')
    while True:
        line = filehandle.readline()
        line = filehandle.readline()
        if "#!/usr/bin/env python3" and "#mqtta" in line:
            print("{}".format(x) + " found")            
            break;
        else:
            print("{}".format(x) + " not found")            
            break;
     
        
filehandle.close()