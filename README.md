# Miranda

This project creates a smarthome environment.

   * <a href="#1 Prepare Raspian">1 Prepare Raspian</a>
   * <a href="#2 Miranda">2 Miranda</a>
      * <a href="#2.1 Installation">2.1 Installation</a>
      * <a href="#2.2 Autostart">2.2 Autostart</a>      
      * <a href="#2.3 Manually Control">2.3 Manually Control</a>
   * <a href="#3 Mosquitto">3 Mosquitto</a>
      * <a href="#3.1 Installation">3.1 Installation</a>   
      * <a href="#3.2 Authentification">3.2 Authentification</a>         
      * <a href="#3.3 Autostart">3.3 Autostart</a>        
   * <a href="#4 Zigbee2MQTT">4 Zigbee2MQTT</a>
      * <a href="#4.1 Installation">4.1 Installation</a>   
      * <a href="#4.2 Configuration">4.2 Configuration</a>   
      * <a href="#4.3 Manually Control">4.3 Manually Control</a>   
      * <a href="#4.4 Pairing">4.4 Pairing</a>   
      * <a href="#4.5 Autostart">4.5 Autostart</a>   
   * <a href="#5 Zigbee2MQTT Coordinator">5 Zigbee2MQTT Coordinator</a>
      * <a href="#5.1 Hardware">5.1 Hardware</a>
      * <a href="#5.2 Flashing">5.2 Flashing</a>
      * <a href="#5.3 Raspberry Pi Connection">5.3 Raspberry Pi Connection</a>
      * <a href="#5.4 Raspberry Pi Configuration">5.4 Raspberry Pi Configuration</a>
   * <a href="#6 Snips.ai Base">6 Snips.ai Base</a>
      * <a href="#6.1 Installation">6.1 Installation</a>   
      * <a href="#6.2 Snips Assistent">6.2 Snips Assistent</a>            


### Features

- flask server 
- control Philips Hue LEDs
- voice control 
- provide a simple script system to create light shows
- read sensors
- share data with ESP8266 moduls by using MQTT
- taskmanagement to automate processes
- watering plants
- SQL-lite database 
- user management and user rights
- smartphone view

</br>
------------
</br>

<a name="1 Prepare Raspian"></a>

### 1 Prepare Raspian 

https://domoticproject.com/extending-life-raspberry-pi-sd-card/
</br>
https://www.antary.de/2018/12/28/raspberry-pi-ein-blick-auf-den-stromverbrauch/
</br>
https://scribles.net/disabling-bluetooth-on-raspberry-pi/
</br>
</br>

- snips supported Raspbian Stretch only !

       >>> https://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2019-04-09/

- activate ssh on your raspberry pi

       >>> sudo raspi-config
       >>> Interfacing Options > SSH > Yes

- establish a network connetion

- open a remote connection 
   
       >>> Putty:

           Raspberry Pi IP-Address
           Port:     22
           User:     pi
           Password: raspberry

- update raspian

       >>> sudo apt-get update && sudo apt-get upgrade -y

- open hostname file and insert new name

       >>> sudo nano /etc/hostname

- disable swap        

       >>> sudo /sbin/dphys-swapfile swapoff

- minimise syslogging 

       >>> sudo nano /etc/rsyslog.conf

           deactivate all logging modules

- remove bluetooth

       >>> sudo apt-get purge bluez -y
       >>> sudo apt-get autoremove -y

- set timezone

       >>> sudo timedatectl set-timezone Europe/Berlin

</br>
------------
</br>

<a name="2 Miranda"></a>

### 2 Miranda

<a name="2.1 Installation"></a>

#### 2.1 Installation 
       
- create the new folder "/home/pi/python" and copy all files into it

       >>> mkdir python

           FileZilla:

           Protocol:   SFTP
           Server:     Raspberry PI IP-Address
           Port:       ---
           Connection: normal
           user:       pi
           password:   raspberry

- install dependencies

       >>> sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran -y
       >>> sudo apt install libhdf5-100 -y
       >>> sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev -y
       >>> sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
       >>> sudo apt-get install libxvidcore-dev libx264-dev -y
       >>> sudo apt-get install libgtk2.0-dev libgtk-3-dev -y

- install graphviz

       >>> sudo apt-get install graphviz libgraphviz-dev pkg-config -y
       >>> sudo apt-get install python-pip python-virtualenv -y

- upgrade pip

       >>> pip3 install --upgrade pip

- install all nessessary python modules

       >>> sudo pip3 install scikit-learn
       >>> sudo pip3 install -r /home/pi/python/requirements.txt --upgrade                                   

- install openCV

       >>> sudo apt install python3-opencv
           (https://raspberrypi.stackexchange.com/questions/100253/how-can-i-install-opencv-on-raspberry-pi-4-raspbian-buster)

- replace wrong spotipy file
 
       >>> sudo cp /home/pi/python/support/spotipy/client.py /usr/local/lib/python3.7/dist-packages/spotipy/client.py

- change folder permissions

       >>> sudo chmod -v -R 070 /home/pi/python

- default_login

       >>> admin
       >>> qwer1234

</br>

<a name="2.2 Autostart"></a>

#### 2.2 Autostart

- create an autostart-file

       >>> sudo nano /etc/systemd/system/miranda.service

           [Unit]
           Description=Miranda
           After=network.target

           [Service]
           ExecStart=/home/pi/python/app.py
           WorkingDirectory=/home/pi
           Restart=always

           [Install]
           WantedBy=multi-user.target

- enable autostart

       >>> sudo systemctl enable miranda.service

- start / stop service

       >>> sudo systemctl start miranda
       >>> sudo systemctl stop miranda

- show status / log

       >>> systemctl status miranda.service
       >>> journalctl -u miranda

</br>

<a name="2.3 Manually Control"></a>

#### 2.3 Manually Control 

- deactivate the miranda service

       >>> sudo systemctl stop miranda

- start the program 

       >>> sudo python3 /home/pi/python/app.py

- stop the program 

       >>> sudo killall python3


</br>
------------
</br>

<a name="3 Mosquitto"></a>

### 3 Mosquitto (MQTT Broker)

https://mosquitto.org/
</br>
https://github.com/eclipse/mosquitto
</br>
https://xperimentia.com/2015/08/20/installing-mosquitto-mqtt-broker-on-raspberry-pi-with-websockets/
</br>
</br>

<a name="3.1 Installation"></a>

#### 3.1 Installation

- install mosquitto

       >>> wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
       >>> sudo apt-key add mosquitto-repo.gpg.key
       >>> cd /etc/apt/sources.list.d/
       >>> sudo wget http://repo.mosquitto.org/debian/mosquitto-stretch.list
       >>> sudo apt-get update
       >>> sudo apt-get install mosquitto

</br>

<a name="3.2 Authentification"></a>

#### 3.2 Authentification

https://medium.com/@eranda/setting-up-authentication-on-mosquitto-mqtt-broker-de5df2e29afc
</br>
</br>

- edit mosquitto config and write these lines

       >>> sudo nano /etc/mosquitto/conf.d/default.conf

           per_listener_settings true

           listener 1883 localhost

           listener 1884
           password_file /etc/mosquitto/passwd
           allow_anonymous false

- change file permissions

       >>> sudo chmod -v -R 060 /etc/mosquitto/passwd

- restart mosquitto

       >>> sudo systemctl restart mosquitto

- verify the authentication

       >>> mosquitto_sub -h localhost -p 1883 -t "test_channel" 
       >>> mosquitto_sub -h localhost -p 1884 -t "test_channel" -u <user_name> -P <password> 

</br>

<a name="3.3 Autostart"></a>

#### 3.3 Autostart

https://forum-raspberrypi.de/forum/thread/31959-mosquitto-autostart/
</br>
</br>

- create an autostart-file

       >>> sudo nano /etc/systemd/system/mosquitto.service

           [Unit]
           Description=MQTT Broker
           After=network.target

           [Service]
           ExecStart=/usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf
           Restart=always

           [Install]
           WantedBy=multi-user.target

- enable autostart

       >>> sudo systemctl enable mosquitto.service

- start / stop service

       >>> sudo systemctl start mosquitto
       >>> sudo systemctl stop mosquitto

- show status / log

       >>> systemctl status mosquitto.service
       >>> journalctl -u mosquitto
       >>> sudo cat /var/log/mosquitto/mosquitto.log

</br>
------------
</br>

<a name="4 ZigBee2MQTT"></a>

### 4 ZigBee2MQTT

https://gadget-freakz.com/diy-zigbee-gateway/
</br>
https://www.zigbee2mqtt.io/
</br>
https://github.com/Koenkk/zigbee2mqtt
</br>

<a name="4.1 Installation"></a>

#### 4.1 Installation

- install Node.js

       >>> sudo curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
       >>> sudo apt-get install -y nodejs git make g++ gcc

- verify that the correct nodejs and npm (automatically installed with nodejs)

       >>> node --version  # Should output v10.X
       >>> npm  --version  # Should output 6.X

- unzip zigbee2mqtt repository

       >>> sudo unzip /home/pi/python/support/zigbee2mqtt_1.6.0.zip -d /opt/zigbee2mqtt
       >>> sudo chown -R pi:pi /opt/zigbee2mqtt

- install zigbee2mqtt 

       >>> cd /opt/zigbee2mqtt
       >>> npm install
	   
	    Note that the npm install produces some warning which can be ignored


##### ERROR: npm not founded

- install the newest version of Node.js 

       >>> https://www.zigbee2mqtt.io/getting_started/running_zigbee2mqtt.html

</br>

<a name="4.2 Configuration"></a>

#### 4.2 Configuration

- change file permissions

       >>> sudo chmod -v -R 070 /opt/zigbee2mqtt/data/configuration.yaml

- generate a network key

       >>> dd if=/dev/urandom bs=1 count=16 2>/dev/null | od -A n -t x1 | awk '{printf "["} {for(i = 1; i< NF; i++) {printf "0x%s, ", $i}} {printf "0x%s]\n", $NF}'

- edit zigbee2mqtt config

       >>> sudo nano /opt/zigbee2mqtt/data/configuration.yaml

           # MQTT settings
           mqtt:
           # MQTT base topic for zigbee2mqtt MQTT messages
           base_topic: miranda/zigbee2mqtt
           # MQTT server URL
           server: 'mqtt://localhost'
           # MQTT server authentication, uncomment if required:
           # user: <my_user>
           # password: <my_password>
           
           advanced:
             network_key: <network_key>

</br>

<a name="4.3 Manually Control"></a>

#### 4.3 Manually Control

- start command

       >>> cd /opt/zigbee2mqtt
       >>> npm start

- stop command

       >>> sudo systemctl stop zigbee2mqtt

- view the log of zigbee2mqtt

       >>> sudo journalctl -u zigbee2mqtt.service -f

- backup configuration

       >>> cp -R data data-backup

</br>

<a name="4.4 Pairing"></a>

#### 4.4 Pairing

- bridge software must be running to pairing new devices automatically
- zigbee2mqtt setting: {permit_join: true}

</br>

<a name="4.5 Autostart"></a>

#### 4.5 Autostart

- create an autostart-file

       >>> sudo nano /etc/systemd/system/zigbee2mqtt.service

           [Unit]
           Description=zigbee2mqtt
           After=network.target

           [Service]
           ExecStart=/usr/bin/npm start
           WorkingDirectory=/opt/zigbee2mqtt
           StandardOutput=inherit
           StandardError=inherit
           Restart=always

           [Install]
           WantedBy=multi-user.target

- enable autostart

       >>> sudo systemctl enable zigbee2mqtt.service

- start / stop service

       >>> sudo systemctl start zigbee2mqtt
       >>> sudo systemctl stop zigbee2mqtt

- show status / log

       >>> systemctl status zigbee2mqtt.service
       >>> journalctl -u zigbee2mqtt

</br>
------------
</br>

<a name="5 Zigbee2MQTT Coordinator"></a>

### 5 Zigbee2MQTT Coordinator

<a name="5.1 Hardware"></a>

#### 5.1 Hardware

- E18-MS1PA1-PCB

       >>> https://de.aliexpress.com/item/32803068018.html

- socket strip (2x5)

       >>> https://www.ebay.de/itm/Zuverlassige-10x-2x5-10Pin-2-54mm-zweireihige-Buchsenleiste-Pitch-Socket-Pin-Fw/254407218443

- internal cables and connectors

       >>> https://www.ebay.de/itm/JST-XH-2-54-Stecker-inkl-15cm-Kabel-XH-Buchse-2-3-4-5-6-7-8-9-10-Pin-24AWG-RC/183748172867

</br>

<a name="5.2 Flashing"></a>

https://github.com/Koenkk/Z-Stack-firmware
</br>
https://github.com/Koenkk/zigbee2mqtt/issues/1437
</br>
</br>

#### 5.2 Flashing (Windows Environment)

- install SmartRF Flash programmer and CC debugger driver (admin rights necessary)

       >>> /devices/E18-MS1PA1-PCB/Flashing/flash-programmer-1.12.8.zip
       >>> /devices/E18-MS1PA1-PCB/Flashing/swrc212a.zip

- connect the debugger to the E18-MS1PA1-PCB 

       >>> CC debugger -> E18-MS1PA1-PCB

           1 -> GND
           2 -> 3,3V
           3 -> P2.2
           4 -> P2.1
           7 -> RESET
           9 -> 3,3V

           connect pin 2 and 9

<p align="center">
  <img src="https://github.com/stanman71/Watering_Control/blob/master/devices/E18-MS1PA1-PCB/Flashing/Programmer%20connection%20to%20E18-MS1PA1-PCB.png">
</p>

</br>

- connect the CC debugger to the PC

- if the light on the CC debugger is RED

       >>> press set reset button on the CC debugger
       >>> if the light is still red, check the connection to the E18-MS1PA1-PCB   

- if the light on the CC debugger is GREEN 

       >>> ready for the next step   

- unzip the firmware files

       >>> /home/pi/miranda/devices/E18-MS1PA1-PCB/z-stack_firmware.zip

- start SmartRF Flash Programmer

       >>> select the new firmware (.hex file)
       >>> don't keep the old ieeeAddr
	>>> select "Erase, program and verify"
       >>> click “Perform actions” 

- if something fails, reset the CC debugger and restart the process

</br>

<a name="5.3 Raspberry Pi Connection"></a>

#### 5.3 Raspberry Pi Connection 

https://www.zigbee2mqtt.io/information/connecting_cc2530.html
</br>
</br>

- Connect the E18-MS1PA1-PCB to the Raspberry

       >>> E18-MS1PA1-PCB -> Raspberry
	   
           VCC -> 3,3V (Pin1)
           GND -> GND  (Pin6)
           P02 -> TXD  (Pin8  / BCM 14)
           P03 -> RXD  (Pin10 / BCM 15)

</br>

<a name="5.4 Raspberry Pi Configuration"></a>

#### 5.4 Raspberry Pi Configuration 

https://www.zigbee2mqtt.io/information/connecting_cc2530.html
</br>
</br>

- add following at the end of the config file

       >>> sudo nano /boot/config.txt 
	   
           enable_uart=1
           dtoverlay=pi3-disable-bt

- disable the modem system service 

       >>> sudo systemctl disable hciuart

- remove any of the following entries in the cmdline file, if present

       >>> sudo nano /boot/cmdline.txt

           console=serial0,115200 
           console=ttyAMA0,115200

- add the lines in zigbee2mqtt config

       >>> sudo nano data/configuration.yaml
	   
           serial:
             port: /dev/ttyAMA0
           advanced:
             baudrate: 115200
             rtscts: false

- reboot your raspberry	

</br>
------------
</br>

<a name="6 Snips.ai Base"></a>

### 6 Snips.ai Base

https://console.snips.ai/login
</br>
https://smarthome-training.com/lokale-sprachsteuerung-mit-openhab-2-und-snips-ai/
</br>
https://docs.snips.ai/getting-started/quick-start-raspberry-pi
</br>
https://docs.snips.ai/articles/platform/satellites
</br>
https://docs.snips.ai/reference/sam#installing-actions-from-the-snips-console
</br>
</br>

<a name="6.1 Installation"></a>

#### 6.1 Installation

- install NodeJs and NPM

       >>> curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
       >>> sudo apt-get install -y nodejs
       >>> node -v -
       >>> npm -v

- install Snipes with SAM

       >>> sudo npm install -g snips-sam
       >>> sam connect raspberrypi.local (raspberry pi name)
       >>> sam init
       >>> sam update

- setup audio devices

       >>> sam setup audio
       >>> sam test speaker
       >>> sam test microphone

- enable or disable audio feedback
	
       >>> sam sound-feedback <on|off>

- checking MQTT messages

       >>> sam watch

- checking the status of the device

       >>> sam status

- install the latest update

       >>> sam update platform

- edit settings
 
       >>> sudo nano /etc/snips.toml

- restart snipes

       >>> sudo systemctl restart snips-*

</br>

<a name="6.2 Snips Assistent"></a>

#### 6.2 Snips Assistent

- create an account on the website, if nessesary

       >>> https://console.snips.ai/signup

- login on the raspberry pi

       >>> sam login

- install the assistant

       >>> sam install assistant

- update the assistant

       >>> sam update-assistant

- installing actions from the Snips Console

       >>> sam install actions

- delete skills

       >>> sudo rm -fr /var/lib/snips/skills/[skill_name]

- installed skills

       >>> https://github.com/MrJohnZoidberg/Snips-Einkaufsliste
       >>> https://github.com/MrJohnZoidberg/Snips-DatumUhrzeit
       >>> https://github.com/michilehr/snips-my-weather
       >>> 