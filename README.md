# Smarthome

This project creates a smarthome environment.

   * <a href="#1 Prepare Raspian">1 Prepare Raspian</a>
   * <a href="#2 Smarthome">2 Smarthome</a>
      * <a href="#2.1 Installation">2.1 Installation</a>
      * <a href="#2.2 Autostart">2.2 Autostart</a>      
      * <a href="#2.3 Manually Control">2.3 Manually Control</a>
   * <a href="#3 NQTT Broker Mosquitto">3 MQTT Broker Mosquitto</a>
      * <a href="#3.1 Installation">3.1 Installation</a>   
      * <a href="#3.2 Autostart">3.2 Autostart</a>           
      * <a href="#3.3 Authentification">3.3 Authentification</a>            
   * <a href="#4 Zigbee2MQTT">4 Zigbee2MQTT</a>
      * <a href="#4.1 Installation">4.1 Installation</a>   
      * <a href="#4.2 Configuration">4.2 Configuration</a>   
      * <a href="#4.3 Manually Control">4.3 Manually Control</a>   
      * <a href="#4.4 Pairing">4.4 Pairing</a>   
      * <a href="#4.5 Autostart">4.5 Autostart</a>   
      * <a href="#4.6 Update">4.6 Update</a>   
   * <a href="#5 Zigbee Coordinator / Router">5 Zigbee Coordinator / Router</a>
      * <a href="#5.1 Hardware">5.1 Hardware</a>
      * <a href="#5.2 Flashing">5.2 Flashing</a>
      * <a href="#5.3 Raspberry Pi installation (coordinator only)">5.3 Raspberry Pi installation (coordinator only)</a>   
   * <a href="#6 Zigbee Devices">6 Zigbee Devices</a>   
      * <a href="#6.1 Supported">6.1 Supported</a>
      * <a href="#6.2 Add new Devices">6.2 Add new Devices</a>        
   * <a href="#7 Logitech Media Server (LMS)">7 Logitech Media Server (LMS)</a>
      * <a href="#7.1 Installation">7.1 Installation</a>
      * <a href="#7.2 Squeezelite Player">7.2 Squeezelite Player</a>
      * <a href="#7.3 LMS Configuration">7.3 LMS Configuration</a>     


### Features

- flask server 
- control Philips Hue LEDs
- voice control 
- provide a simple script system to create light shows
- read sensors
- share data with ESP8266 moduls by using MQTT
- taskmanagement to automate processes
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

- change hostname 

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

<a name="2 Smarthome"></a>

### 2 Smarthome

<a name="2.1 Installation"></a>

#### 2.1 Installation 
       
- create the new folder "/home/pi/smarthome" and copy all files into it

       >>> mkdir smarthome

           FileZilla:

           Protocol:   SFTP
           Server:     Raspberry PI IP-Address
           Port:       ---
           Connection: normal
           user:       pi
           password:   raspberry

- install dependencies

       >>> sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran -y
       >>> sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev -y
       >>> sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
       >>> sudo apt-get install libxvidcore-dev libx264-dev -y
       >>> sudo apt-get install libgtk2.0-dev libgtk-3-dev -y

- install graphviz

       >>> sudo apt-get install graphviz libgraphviz-dev pkg-config -y
       >>> sudo apt-get install python-pip python-virtualenv -y

- upgrade pip

       >>> sudo apt install python3-pip -y

- install all nessessary python modules

       >>> sudo pip3 install scikit-learn
       >>> sudo pip3 install -r /home/pi/smarthome/requirements.txt --upgrade                                   

- install openCV

       >>> sudo apt install python3-opencv -y
           (https://raspberrypi.stackexchange.com/questions/100253/how-can-i-install-opencv-on-raspberry-pi-4-raspbian-buster)

- replace wrong spotipy file
 
       >>> sudo cp /home/pi/smarthome/support/spotipy/client.py /usr/local/lib/python3.7/dist-packages/spotipy/client.py

- change folder permissions

       >>> sudo chmod -v -R 070 /home/pi/smarthome

- default_login

       >>> admin
       >>> qwer1234

</br>

<a name="2.2 Autostart"></a>

#### 2.2 Autostart

- create an autostart-file

       >>> sudo nano /etc/systemd/system/smarthome.service

           [Unit]
           Description=Smarthome
           After=network.target

           [Service]
           ExecStart=/home/pi/smarthome/app.py
           WorkingDirectory=/home/pi
           Restart=always

           [Install]
           WantedBy=multi-user.target

- enable autostart

       >>> sudo systemctl enable smarthome.service

- start / stop service

       >>> sudo systemctl start smarthome
       >>> sudo systemctl stop smarthome

- show status / log

       >>> systemctl status smarthome.service
       >>> journalctl -u smarthome

</br>

<a name="2.3 Manually Control"></a>

#### 2.3 Manually Control 

- deactivate the smarthome service

       >>> sudo systemctl stop smarthome

- start the program 

       >>> sudo python3 /home/pi/smarthome/app.py

- stop the program 

       >>> sudo killall python3


</br>
------------
</br>

<a name="3 NQTT Broker Mosquitto"></a>

### 3 NQTT Broker Mosquitto

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
       >>> sudo wget http://repo.mosquitto.org/debian/mosquitto-buster.list
       >>> sudo apt-get update
       >>> sudo apt-get install mosquitto -y
       >>> sudo apt-get install mosquitto-clients -y


</br>

<a name="3.2 Autostart"></a>

#### 3.2 Autostart

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

<a name="3.3 Authentification"></a>

#### 3.3 Authentification

https://medium.com/@eranda/setting-up-authentication-on-mosquitto-mqtt-broker-de5df2e29afc
</br>
</br>

- create an user

       >>> sudo mosquitto_passwd -c /etc/mosquitto/passwd [username]

- edit mosquitto config and write these lines

       >>> sudo nano /etc/mosquitto/conf.d/default.conf

           per_listener_settings true

           listener 1883 localhost

           listener 1884
           password_file /etc/mosquitto/passwd
           allow_anonymous false

- restart mosquitto

       >>> sudo systemctl restart mosquitto

- test mosquitto authentification

       >>> mosquitto_sub -h localhost -p 1883 -t "test_channel" 
       >>> mosquitto_sub -h localhost -p 1884 -t "test_channel" -u <user_name> -P <password> 

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
</br>

<a name="4.1 Installation"></a>

#### 4.1 Installation

- install Node.js

       >>> sudo curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
       >>> sudo apt-get install -y nodejs git make g++ gcc

- verify that the correct nodejs and npm (automatically installed with nodejs)

       >>> node --version  # Should output v10.X
       >>> npm  --version  # Should output 6.X

- clone zigbee2mqtt repository

       >>> sudo git clone https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
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
home
- generate a network key

       >>> dd if=/dev/urandom bs=1 count=16 2>/dev/null | od -A n -t x1 | awk '{printf "["} {for(i = 1; i< NF; i++) {printf "0x%s, ", $i}} {printf "0x%s]\n", $NF}'

- edit zigbee2mqtt config

       >>> sudo nano /opt/zigbee2mqtt/data/configuration.yaml

           homeassistant: false

           # deactivate joining of new devices
           permit_join: false

           # MQTT settings
           mqtt:
           # MQTT base topic for zigbee2mqtt MQTT messages
           base_topic: smarthome/zigbee2mqtt
           # MQTT server URL
           server: 'mqtt://localhost'
           # MQTT server authentication, uncomment if required:
           # user: <my_user>
           # password: <my_password>
       
           advanced:
             network_key: [network_key]
             log_directory: /home/pi/smarthome/data/logs/zigbee2mqtt/

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

- joining of new devices is deactivate
- you have to active the joining in smarthome / settings / devices
- zigbee2mqtt setting to allow joining: {permit_join: true}

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

<a name="4.6 Update"></a>

#### 4.6 Update

https://www.zigbee2mqtt.io/getting_started/running_zigbee2mqtt.html
</br>
</br>

- run the follwing commands to install the latest zigbee2mqtt version

       >>> sudo systemctl stop zigbee2mqtt
       >>> cd /opt/zigbee2mqtt
       >>> sudo cp -R data data-backup
       >>> git checkout HEAD -- npm-shrinkwrap.json
       >>> git pull
       >>> rm -rf node_modules
       >>> npm install
       >>> sudo cp -R data-backup/* data
       >>> sudo rm -rf data-backup
       >>> sudo systemctl start zigbee2mqtt

</br>
------------
</br>

<a name="5 Zigbee2MQTT Coordinator / Router"></a>

### 5 Zigbee2MQTT Coordinator / Router

https://www.zigbee2mqtt.io/information/zigbee_network.html
</br>
</br>

<a name="5.1 Hardware"></a>

#### 5.1 Hardware

- E18-MS1PA1-PCB

       >>> https://de.aliexpress.com/item/32803068018.html

- socket strip (2x5)

       >>> https://www.ebay.de/itm/273382759328?ViewItem=&item=273382759328

- internal cables and connectors

       >>> https://www.ebay.de/itm/JST-XH-2-54-Stecker-inkl-15cm-Kabel-XH-Buchse-2-3-4-5-6-7-8-9-10-Pin-24AWG-RC/183748172867

- voltage regulator 3.3V (router only)

       >>> https://www.ebay.de/itm/Spannungsregler-Modul-AMS1117-3-3V-800mA-Arduino-Raspberry-Pi-Atmega/152386958012

- power connector (router only)

       >>> https://www.berrybase.de/bauelemente/steckverbinder/stromversorgungs-steckverbinder/dc-stecker-hohlstecker/dc-einbaubuchse-f-252-r-hohlstecker-5-5x2-5mm-metallausf-252-hrung-l-246-tanschluss?c=115

- power source (router only)

       >>> https://www.amazon.de/LEICKE-Netzteil-Universal-2-5mm-Stecker/dp/B01I1JEWPU/ref=sr_1_15?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=netzteil%2BWS2811&qid=1571760422&sr=8-15&th=1

- case

       >>> https://www.tme.eu/de/details/abs-54p/universal-gehause/maszczyk/km-54p-gy/
       >>> https://www.tme.eu/de/details/km-54p/universal-gehause/maszczyk/km-54p-bk/

</br>

<a name="5.2 Flashing"></a>

https://github.com/Koenkk/Z-Stack-firmware
</br>
https://github.com/Koenkk/zigbee2mqtt/issues/1437
</br>
</br>

#### 5.2 Flashing (Windows Environment)

- install SmartRF Flash programmer and CC debugger driver (admin rights necessary)

       >>> /devices/zigbee_coordinator_router/Flashing/flash-programmer-1.12.8.zip
       >>> /devices/zigbee_coordinator_router/Flashing/swrc212a.zip

- connect the debugger to the E18-MS1PA1-PCB Board

       >>> CC debugger -> E18-MS1PA1-PCB

           1 -> GND
           2 -> 3,3V
           3 -> P2.2
           4 -> P2.1
           7 -> RESET
           9 -> 3,3V

           connect pin 2 and 9

<p align="center">
  <img src="https://github.com/stanman71/Watering_Control/blob/master/zigbee_coordinator/soldering/Flashing/Programmer%20connection%20to%20E18-MS1PA1-PCB.png">
</p>

</br>

- connect the CC debugger to the PC

- if the light on the CC debugger is RED

       >>> press set reset button on the CC debugger
       >>> if the light is still red, check the connection to the E18-MS1PA1-PCB   

- if the light on the CC debugger is GREEN 

       >>> ready for the next step   

- unzip the firmware files

       >>> /home/pi/smarthome/devices/zigbee_coordinator_router/z-stack_firmware.zip

- start SmartRF Flash Programmer

       >>> select a coordinator / router firmware (.hex file)
       >>> don't keep the old ieeeAddr
	>>> select "Erase, program and verify"
       >>> click “Perform actions” 

- if something fails, reset the CC debugger and restart the process

</br>

<a name="5.3 Raspberry Pi installation (coordinator only)"></a>

#### 5.3 Raspberry Pi installation (coordinator only)

https://www.zigbee2mqtt.io/information/connecting_cc2530.html
</br>
</br>

- connect the coordinator to the Raspberry Pi

       >>> coordinator -> Raspberry Pi
	   
                   VCC -> 3,3V (Pin1)
                   GND -> GND  (Pin6)
                   P02 -> TXD  (Pin8  / BCM 14)
                   P03 -> RXD  (Pin10 / BCM 15)

- start the Raspberry Pi

- add following at the end of the config file

       >>> sudo nano /boot/config.txt 
	   
           [zigbee]
           enable_uart=1
           dtoverlay=pi3-disable-bt

- disable the modem system service 

       >>> sudo systemctl disable hciuart

- remove any of the following entries in the cmdline file, if present

       >>> sudo nano /boot/cmdline.txt

           console=serial0,115200 
           console=ttyAMA0,115200

- add the lines in zigbee2mqtt config

       >>> sudo nano /opt/zigbee2mqtt/data/configuration.yaml
	   
           serial:
             port: /dev/ttyAMA0
           advanced:
             baudrate: 115200
             rtscts: false

- reboot your raspberry	

</br>
------------
</br>

<a name="6 Zigbee Devices"></a>

### 6 Zigbee Devices

<a name="6.1 Supported"></a>

#### 6.1 Supported

- Eurotronic heater thermostat (SPZB0001)
- IKEA TRADFRI LED bulb E27 980 lumen (LED1545G12)
- IKEA TRADFRI LED bulb E27 950 lumen (LED1546G12)
- IKEA TRADFRI LED bulb E27 1000 lumen (LED1623G12)
- IKEA TRADFRI LED bulb GU10 400 lumen (LED1537R6)
- IKEA TRADFRI LED bulb GU10 400 lumen (LED1650R5)
- IKEA TRADFRI LED bulb E14 400 lumen (LED1536G5)
- IKEA TRADFRI LED bulb GU10 400 lumen (LED1837R5)
- IKEA TRADFRI LED bulb E27 WW clear 250 lumen (LED1842G3)
- IKEA TRADFRI LED bulb E14 600 lumen (LED1733G7)
- IKEA TRADFRI LED bulb E14/E27 600 lumen (LED1624G9)
- IKEA TRADFRI LED bulb E14 400 lumen (LED1649C5)
- IKEA TRADFRI LED bulb E27 1000 lumen (LED1732G11)
- IKEA TRADFRI LED bulb E27 806 lumen (LED1736G9 / LED1836G9)
- IKEA LEPTITER Recessed spot light (T1820)
- IKEA TRADFRI driver for wireless control (10 watt) (ICPSHC24-10EU-IL-1)
- IKEA TRADFRI driver for wireless control (30 watt) (ICPSHC24-30EU-IL-1)
- IKEA FLOALT LED light panel (L1527 / L1528 / L1529)
- IKEA GUNNARP panel 40*40" (T1829)
- IKEA SURTE door light panel (L1531)
- IKEA TRADFRI control outlet (E1603 / E1702)
- IKEA TRADFRI motion sensor (E1525)
- IKEA TRADFRI signal repeater (E1746)
- IKEA FYRTUR roller blind (E1757)
- IKEA KADRILJ roller blind (E1926)
- IKEA TRADFRI remote control (E1524 / E1810)
- IKEA SYMFONISK sound controller (E1744)
- IKEA TRADFRI open/close remote (E1766)
- LEDVANCE Smart+ Plug (AC10691)
- Philips Hue Bloom (7299760PH)
- Philips Hue Go (7146060PH)
- PHILIPS HUE White & Color Ambiance GU10 (929001953101)
- Philips Hue white A60 bulb E27 (9290011370)
- Philips Hue White & Color Ambiance E14/E27 (9290012573A / 9290022166)
- Philips Hue white ambiance E27 with Bluetooth (9290022169)
- Philips Hue white GU10 (LWG004)
- Philips Hue white GU10 with Bluetooth (9290018195)
- Philips Hue white and color ambiance LightStrip (915005106701)
- Philips Hue white and color ambiance GU10 (8718696485880)
- Philips Hue White and color ambiance Play Lightbar (915005733701)
- Philips Hue white ambiance E14 (8718696695203)
- Philips Hue Iris (7199960PH)
- Philips LivingColors Aura (7099860PH)
- Philips Hue smart plug EU (929002240401)
- Philips Hue motion sensor (9290012607)
- Philips Hue motion sensor outdoor (9290019758)
- OSRAM Smart+ Plug (AB3257001NJ)
- Xiaomi AQARA contact sensor (MCCGQ11LM)
- Xiaomi AQARA water leak sensor (SJCGQ11LM)
- Xiaomi MiJia temperature and humidity sensor (WSDCGQ01LM)
- Xiaomi Aqara temperature, humidity and pressure sensor (WSDCGQ11LM)
- Xiaomi Aqara vibration sensor (DJT11LM)
- Xiaomi AQARA Wireless Switch (WXKG11LM)
- Xiaomi Aqara Opple switch 1 band (WXCJKG11LM)
- Xiaomi Aqara Opple switch 2 band (WXCJKG12LM)
- Xiaomi Aqara Opple switch 3 band (WXCJKG13LM)

</br>

<a name="6.2 Add new Devices"></a>

#### 6.2 Add new Devices

- go the to overview of all possible devices

       >>> https://www.zigbee2mqtt.io/information/supported_devices.html

- get the model number and basic informations (input_values, input_events, commands)

- add the new device in the config file

       >>> /home/pi/smarthome/data/zigbee_device_informations.json


</br>
------------
</br>

<a name="7 Logitech Media Server (LMS)"></a>

### 7 Logitech Media Server (LMS)

https://www.hagensieker.com/wordpress/2018/06/12/302/
</br>
http://downloads.slimdevices.com/nightly/7.9/sc/
</br>
</br>

<a name="7.1 Installation"></a>

#### 7.1 Installation

- install dependencies 

       >>> sudo apt-get install libio-socket-ssl-perl libnet-libidn-perl libnet-ssleay-perl perl-openssl-defaults

- install LMS

       >>> sudo dpkg -i /home/pi/smarthome/support/logitechmediaserver_7.9.2~1574959426_arm.deb

- enable autostart

       >>> sudo systemctl enable logitechmediaserver

</br>

<a name="7.2 Squeezelite Player"></a>

#### 7.2 Squeezelite Player

- create a multiroom group placeholder

- install dependencies

       >>> sudo apt-get install libasound2-dev libflac-dev libmad0-dev libvorbis-dev libfaad-dev libmpg123-dev liblircclient-dev libncurses5-dev -y

- install squeezelite

       >>> sudo apt install /home/pi/smarthome/support/squeezelite_1.8-4.1+b1_armhf.deb -y

- squeezelite config 

       >>> sudo nano /etc/default/squeezelite 

           SL_NAME="multiroom"

           # ALSA output device:
	    SL_SOUNDCARD="hw:CARD=ALSA,DEV=0"

- enable autostart

       >>> sudo systemctl enable squeezelite

</br>

<a name="7.3 LMS Configuration"></a>

#### 7.3 LMS Configuration 

- open LMS web-gui

       IP-address:  raspberry pi address
       defaultport: 9000

- skip logitech account creation

- install spotty plugin

       >>> settings / plugins / Spotty  

- config spotty

       >>> add premium account 
       >>> activate local placeholder player "multiroom" at spotify connect only
       >>> activate option "Überwache die Verbindung der Spotty Connect Helferanwendung"    
          
       >>> multiroom group is now selectable in spotify

- synchronize players

       >>> set the player-groups on the main page in the upper-right corner 
           (Squeezelite must be installed and running on the clients)
       >>> synchronize all squeezelite clients with the multiroom group