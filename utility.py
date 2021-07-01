import socket
import psutil
import subprocess
import time
import logging
import os
import json
import core

class Utility:
    
    logText = ""
    
    def util(self, setEol, trace_routes, hostname, setUsername, setPassword, cpu_usage, ram_usage, ipAddr, storage_used_total, used_percentage2, res, logText, DynamicVar, changeHostname, setBroker, logFile, subTopic):
        self.hostname = hostname
        self.setUsername = setUsername
        self.setPassword = setPassword
        self.cpu_usage = cpu_usage
        self.ram_usage = ram_usage
        self.ipAddr = ipAddr
        self.storage_used_total = storage_used_total
        self.used_percentage2 = used_percentage2
        self.res = res
        self.logText = logText
        self.DynamicVar = DynamicVar
        self.changeHostname = changeHostname
        self.trace_routes = trace_routes
        self.setBroker = setBroker
        self.logFile = logFile
        self.subTopic = subTopic
        self.setEol = setEol
    
    def eol(self):
        filename = "setup.config"
        contents = open(filename).read()
        config = eval(contents)
        eol = config['eolFile']
        f = open(eol, 'r')
        f2 = f.readline()
        self.setEol = f2
        return self.setEol

    def subtopic(self):
        p = core.MyApp()
        m = p.run.lastWord
        self.subTopic = m
        return self.subTopic

    def broker(self):
        filename = "setup.config"
        contents = open(filename).read()
        config = eval(contents)
        broker = config['broker']
        self.setBroker = broker
        return(self.setBroker)

    def username(self):
        filename = "setup.config"
        contents = open(filename).read()
        config = eval(contents)
        username = config['username']
        self.setUsername = username
        return(self.setUsername)

    def password(self):
        filename = "setup.config"
        contents = open(filename).read()
        config = eval(contents)
        password = config['password']
        self.setPassword = password
        return(self.setPassword)

    def trace(self):
        p = core.MyApp()
        m = p.run.trace_route_target
        self.trace_routes = m
        return self.trace_routes

    def changehostname(self):
        p = core.MyApp()
        m = p.run.hostname
        self.changeHostname = m
        return self.changeHostname

    def DynamicVariable(self):
        p = core.MyApp()
        m = p.run.DynamicVar
        self.DynamicVar = m
        return self.DynamicVar
        
    def host(self):
        self.hostname = socket.gethostname()
        return self.hostname


    def ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        self.ipAddr = s.getsockname()[0]
        s.close()
        return self.ipAddr


    def cpu(self):
        self.cpu_usage = str(psutil.cpu_percent())
        return self.cpu_usage


    def ram(self):        
        self.ram_usage = str(psutil.virtual_memory().percent)
        return self.ram_usage


    def storage(self):
        hdd = psutil.disk_usage('/')
        total = (hdd.total / (2**30))
        used = (hdd.used / (2**30))
        format_total = '{0:.3g}'.format(total)
        format_used = '{0:.3g}'.format(used)
        self.storage_used_total = str(format_used) + "GB" + " " + str(format_total) + "GB"
        used_percentage = float(format_used) / float(format_total) * 100
        self.used_percentage2 = '{0:.3g}'.format(used_percentage)
#        strg = str(self.storage_used_total + " " + self.used_percentage2 + "%" + "used")
        strg = str(self.used_percentage2)
        return strg


    def uptime(self):
        uptime = (float)(subprocess.check_output(['cat', '/proc/uptime']).decode('utf-8').split()[0])
        sec = uptime
        ty_res = time.gmtime(sec)
        self.res = time.strftime("%H:%M:%S", ty_res)
        return self.res


    def log(self):
        filename = "setup.config"
        contents = open(filename).read()
        config = eval(contents)
        loglocation = config['logFile']
        self.logFile = loglocation
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
        file_handler = logging.FileHandler(self.logFile + "/mqtta.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info(str(self.logText))


    def system(self):
        u = Utility()
        ip = u.ip()
        hostt = u.host()
        cpu = u.cpu()
        ram = u.ram()
        strg = u.storage()
        up = u.uptime()

        system = {
            "Hostname": f'{hostt}',
            "IP": f'{ip}',
            "CPU usage": f'{cpu}',
            "MEM usage": f'{ram}',
            "Storage": f'{strg}',
            "SystemUptime": f'{up}'
            }
        
        json_system = json.dumps(system, indent=4)
        self.system = json_system
        return self.system