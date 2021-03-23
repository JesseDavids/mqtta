# MQTT-AGENT

## The program plugin-architecture was created to retrieve information from computers via mqtt
The program has been tested on ubuntu 20.04 and the lastest Linux Mint as of 03/17/2021
Windows version coming soon...

## The program comes with free to use plugins

   - report_plugin (reports your system information back to you)
   - hostname_plugin (allows you to change your hostname)
   - ping_plugin (lets you ping a specific IP address)
   - traceroute_plugin (Enjoy traceroute to a website or IP address, in order to use this plugin you need to install traceroute on your computer `sudo apt install traceroute`.
   - reboot_plugin (Remotely reboot your system)
   - shutdown_plugin (Or shut it down completely)
   - list_plugin (this plugin lists all available computers connected to the broker, when used, all computers return their hostname and ip address)
    - `workstation/list_plugin/`


###### With this information, coupled with good management software such as mqtt explorer the possibilities are endless
  - ![image](https://user-images.githubusercontent.com/54505758/111479643-d61c5a00-8739-11eb-9228-be9bee8b32c4.png)


## INSTRUCTIONS

- Ensure the `mqtt broker`, and `pip3` is installed before proceeding with these tasks
  - Follow these links on how to do that:
    - and use this command to install the client broker `sudo apt install mosquitto-clients`
    - https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/
    - NOTE: Pip comes with the installation of python3.X
- _____________________________________________________________________________________________________________________________
- Create a folder in your `Documents folder` (or wherever) and pull the repo into that folder then `cd` into it
- Install any requirements from the requirements.txt file `pip3 install -r requirements.txt`(My current version of pip is 20.0.2)
- Open the config file `setup.config` and edit the broker IP address and file path to save the logs
- You can run it in two ways, firstly, you can type in the terminal `./main.py` and run it like that, or
- You could run it as a `service`, to do this i made a `.service` file with basic configurations called `mqtta.service`.
- Open the service file and edit it to your environment with `nano mqtta.service`
- Save the service file in the `/etc/systemd/system/` directory
- Then run this command `systemctl start mqtta.service`
- Refresh daemon with `systemctl daemon-reload`
- If you would like the service to start on boot run this command after the above command, `systemctl enable mqtta.service`
- Restart the service with, `systemctl restart mqtta.service` then check the status, `systemctl status mqtta.service`


## After everything is set and configured, let's test it
- open a terminal and type in `mosquitto_sub -h 127.0.0.1 -t "#"`
  - (-h) this indicates which host we are connecting to
  - (-t) this is the topic we are subscribing to, and `# = hash` means everything, so we will receive any message that comes through

- 3 parameters exist, `(n = notice, r = read, w = write)`

- open another terminal and type `mosquitto_pub -h 127.0.0.1 -t "workstation/your-hostname/parameter/report_plugin/ -m ""`
  - expected output:
    - ![image](https://user-images.githubusercontent.com/54505758/111478420-bd5f7480-8738-11eb-858e-cbc2e6315e43.png)

  - If you want this to work the IP needs to be your own, or another IP on the same network connected to the mqtt broker
  - (-m) this indicates the message you want to send to that particular topic, some plugins do not need a message as the report_plugin
- Here is another example `mosquitto_pub -h 127.0.0.1 -t "workstation/hostname-or-ip/r/ping_plugin/ -m "1.1.1.1 10 0.2"`
  - Note the -m (message). IP {space} Count {space} Interval
    - ![image](https://user-images.githubusercontent.com/54505758/111478776-0a434b00-8739-11eb-9270-38957ff9e026.png)
