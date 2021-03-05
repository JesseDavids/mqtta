import socket
import psutil
import subprocess
import time
import logging
import os
import core
#import paho.mqtt.client as mqtt

class Utility:
    logText = ""
    broker = ""

    def util(self, hostname, cpu_usage, ram_usage, ipAddr, storage_used_total, used_percentage2, res, logText, pingSet, changeHostname):
        self.hostname = hostname
        self.cpu_usage = cpu_usage
        self.ram_usage = ram_usage
        self.ipAddr = ipAddr
        self.storage_used_total = storage_used_total
        self.used_percentage2 = used_percentage2
        self.res = res
        self.logText = logText
        self.pingSet = pingSet
        self.changeHostname = changeHostname

    def changehostname(self):
        p = core.MyApp()
        m = p.run.hostname
        self.changeHostname = m
        return self.changeHostname

    def ping(self):
        p = core.MyApp()
        m = p.run.pingSetting
        self.pingSet = m
        return self.pingSet
        
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
        self.cpu_usage = str(psutil.cpu_percent()) + "%"
        return self.cpu_usage


    def ram(self):        
        self.ram_usage = str(psutil.virtual_memory().percent) + " %"
        return self.ram_usage


    def storage(self):
        hdd = psutil.disk_usage('/')
        total = (hdd.total / (2**30))
        used = (hdd.used / (2**30))
        format_total = '{0:.3g}'.format(total)
        format_used = '{0:.3g}'.format(used)
        self.storage_used_total = str(format_used) + " GB" + " / " + str(format_total) + " GB"
        used_percentage = float(format_used) / float(format_total) * 100
        self.used_percentage2 = '{0:.3g}'.format(used_percentage)
        strg = str(self.storage_used_total + " / " + self.used_percentage2 + " %" + " used ")
        return strg


    def uptime(self):
        uptime = (float)(subprocess.check_output(['cat', '/proc/uptime']).decode('utf-8').split()[0])
        sec = uptime
        ty_res = time.gmtime(sec)
        self.res = time.strftime("%H:%M:%S", ty_res)
        return self.res


    def log(self):
        
        logger = logging.getLogger(__name__)

        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
        p_p = os.getcwd()
        file_handler = logging.FileHandler(p_p + "/mqtta.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        #logger.info(str(system))
        #return self.logText
        logger.info(str(self.logText))


    def system(self):
        u = Utility()
        ip = u.ip()
        hostt = u.host()
        cpu = u.cpu()
        ram = u.ram()
        strg = u.storage()
        up = u.uptime()

        system = {}
        system['system info'] = []
        system['system info'].append({
            'Hostname': hostt,
            'IP': ip,
            'CPU usage': cpu,
            'MEM usage': ram,
            'Storage': strg,
            'SystemUptime': up})
        self.system = system
        return self.system
        #print(str(system))


#u = Utility()
#u.log()
#u.system()

