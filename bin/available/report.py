
def on_message(client, userdata, message):
    
    if(topic == "workstation/{}/r/report".format(ip)):
		client.publish("workstation/{}/n/report".format(ip), str(system) , 2, False)			
		logger.info(str(system))