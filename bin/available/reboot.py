
def on_message(client, userdata, message):

    if(topic == "workstation/{}/w/reboot".format(ip)):
			client.publish("workstation/{}/n/reboot".format(ip), somejson, 2, False)
			logger.info("System is rebooting..")
			time.sleep(2)
			os.system("reboot")