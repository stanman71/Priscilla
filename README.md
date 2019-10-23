# Miranda

This project creates a smarthome environment.

   * <a href="#1 Miranda">1 Miranda</a>
      * <a href="#1.1 Installation">1.1 Installation</a>
      * <a href="#1.2 Autostart">1.2 Autostart</a>      
      * <a href="#1.3 Manually Control">1.3 Manually Control</a>
   * <a href="#2 Mosquitto">2 Mosquitto</a>
      * <a href="#2.1 Installation">2.1 Installation</a>   
      * <a href="#2.2 Test">2.2 Test</a>    
      * <a href="#2.3 Autostart">2.3 Autostart</a>   
      * <a href="#2.4 Authentification">2.4 Authentification</a>          
   * <a href="#3 Zigbee2MQTT">3 Zigbee2MQTT</a>
      * <a href="#3.1 Installation">3.1 Installation</a>   
      * <a href="#3.2 Configuration">3.2 Configuration</a>   
      * <a href="#3.3 Manually Control">3.3 Manually Control</a>   
      * <a href="#3.4 Pairing">3.4 Pairing</a>   
      * <a href="#3.5 Autostart">3.5 Autostart</a>   
   * <a href="#4 Zigbee2MQTT Hardware">4 Zigbee2MQTT Hardware</a>
      * <a href="#4.1 Flashing E18-MS1PA1-PCB">4.1 Flashing E18-MS1PA1-PCB</a>
      * <a href="#4.2 Raspberry Pi Connection">4.2 Raspberry Pi Connection</a>
      * <a href="#4.3 Raspberry Pi Configuration">4.3 Raspberry Pi Configuration</a>

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

<a name="1 Miranda"></a>

### 1 Miranda

<a name="1.1 Installation"></a>

#### 1.1 Installation 

- activate ssh

       >>> sudo raspi-config
       >>> Interfacing Options > SSH > Yes

- update raspian

       >>> sudo apt-get update && sudo apt-get upgrade

- upgrade pip

       >>> pip install --upgrade pip

- open hostname file and insert new name

       >>> sudo nano /etc/hostname
           miranda
          
- create the new folder "/home/pi/miranda" and copy all Miranda files into it

       >>> mkdir miranda

       FileZilla

       Protocol:   SFTP
       Server:     Raspberry PI IP-Address
       Port:       ---
       Connection: normal
       user:       pi
       password:   raspberry

- install BLAS and LAPACK

       >>> sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran

- install graphviz

       >>> sudo apt-get install graphviz libgraphviz-dev pkg-config
       >>> sudo apt-get install python-pip python-virtualenv

- install all nessessary python modules

       >>> sudo pip3 install -r /home/pi/miranda/requirements.txt --upgrade

- install openCV

       >>> sudo apt install python3-opencv
           (https://raspberrypi.stackexchange.com/questions/100253/how-can-i-install-opencv-on-raspberry-pi-4-raspbian-buster)

- replace wrong spotipy file
 
       >>> sudo cp /home/pi/miranda/support/spotipy/client.py /usr/local/lib/python3.7/dist-packages/spotipy/client.py

- change folder permissions

       >>> sudo chmod -v -R 070 /home/pi/miranda

- default_login

       >>> admin
       >>> qwer1234

</br>

<a name="1.2 Autostart"></a>

#### 1.2 Autostart

- create an autostart-file

       >>> sudo nano /etc/systemd/system/miranda.service

           [Unit]
           Description=Miranda
           After=network.target

           [Service]
           ExecStart=/home/pi/miranda/run.py
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

<a name="1.3 Manually Control"></a>

#### 1.3 Manually Control 

- deactivate the miranda service

       >>> sudo systemctl stop miranda

- start the program 

       >>> sudo python3 /home/pi/miranda/run.py

- stop the program 

       >>> sudo killall python3


</br>
------------
</br>

<a name="2 Mosquitto"></a>

### 2 Mosquitto (MQTT)

https://mosquitto.org/
</br>
https://forum-raspberrypi.de/forum/thread/31959-mosquitto-autostart/
</br>
https://github.com/eclipse/mosquitto
</br>
https://medium.com/@eranda/setting-up-authentication-on-mosquitto-mqtt-broker-de5df2e29afc
</br>
https://www.auxnet.de/verschluesseltes-mqtt-vom-und-zum-mosquitto-server/
</br>

<a name="2.1 Installation"></a>

#### 2.1 Installation

       >>> sudo apt-get install mosquitto mosquitto-clients -y

</br>

<a name="2.2 Test"></a>

#### 2.2 Test

- subscribe a channel

       >>> mosquitto_sub -d -h localhost -p 1883 -t "test_channel"

- send a message

       >>> mosquitto_pub -d -h localhost -p 1883 -t "test_channel" -m "Hello World"

</br>

<a name="2.3 Autostart"></a>

#### 2.3 Autostart

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

<a name="2.4 Authentification"></a>

#### 2.4 Authentification

- stop mosquitto

       >>> sudo systemctl stop mosquitto

- create a new user and password

       >>> sudo mosquitto_passwd -c /etc/mosquitto/passwd <user_name>

- change file permissions

       >>> sudo chmod -v -R 060 /etc/mosquitto/passwd

- edit mosquitto config and add these two lines

       >>> sudo nano /etc/mosquitto/mosquitto.conf

           password_file /etc/mosquitto/passwd
           allow_anonymous false

- restart mosquitto

       >>> sudo systemctl restart mosquitto

- verify the authentication

       >>> mosquitto_sub -h localhost -p 1883 -t "test_channel" -u <user_name> -P <password>
       >>> mosquitto_pub -h localhost -p 1883 -t "test_channel" -u <user_name> -P <password> -m "Hello World"

</br>
------------
</br>

<a name="3 ZigBee2MQTT"></a>

### 3 ZigBee2MQTT

https://gadget-freakz.com/diy-zigbee-gateway/
</br>
https://www.zigbee2mqtt.io/
</br>
https://github.com/Koenkk/zigbee2mqtt
</br>

<a name="3.1 Installation"></a>

#### 3.1 Installation

- install Node.js

       >>> sudo curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
       >>> sudo apt-get install -y nodejs git make g++ gcc

- verify that the correct nodejs and npm (automatically installed with nodejs)

       >>> node --version  # Should output v10.X
       >>> npm  --version  # Should output 6.X

- clone zigbee2mqtt repository

       >>> sudo unzip /home/pi/miranda/support/files/zigbee2mqtt_1.6.0.zip -d /opt/zigbee2mqtt
       >>> sudo chown -R pi:pi /opt/zigbee2mqtt

- install zigbee2mqtt 

       >>> cd /opt/zigbee2mqtt
       >>> npm install
	   
	   Note that the npm install produces some warning which can be ignored


##### ERROR: npm not founded

- install the newest version of Node.js 

       >>> https://www.zigbee2mqtt.io/getting_started/running_zigbee2mqtt.html

</br>

<a name="3.2 Configuration"></a>

#### 3.2 Configuration

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
           user: <my_user>
           password: <my_password>
           
           advanced:
             network_key: <network_key>

</br>

<a name="3.3 Manually Control"></a>

#### 3.3 Manually Control

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

<a name="3.4 Pairing"></a>

#### 3.4 Pairing

- bridge software must be running to pairing new devices automatically
- zigbee2mqtt setting: {permit_join: true}

</br>

<a name="3.5 Autostart"></a>

#### 3.5 Autostart

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

<a name="4 Zigbee2MQTT Hardware"></a>

### 4 Zigbee2MQTT Hardware

https://www.zigbee2mqtt.io/information/connecting_cc2530.html
</br>
https://github.com/Koenkk/Z-Stack-firmware
</br>
https://github.com/Koenkk/zigbee2mqtt/issues/1437
</br>
https://de.aliexpress.com/item/32803068018.html?spm=a2g0x.search0604.3.1.72bf1da4p5aRPJ&ws_ab_test=searchweb0_0,searchweb201602_4_10065_10068_10547_319_317_10548_10696_10084_453_10083_454_10618_10304_10307_10820_10821_537_10302_536_10843_10059_10884_10887_321_322_10103,searchweb201603_52,ppcSwitch_0&algo_expid=b4469d30-8afc-4863-971b-96231ae6da3e-0&algo_pvid=b4469d30-8afc-4863-971b-96231ae6da3e
</br>
</br>

<a name="4.1 Flashing E18-MS1PA1-PCB"></a>

#### 4.1 Flashing E18-MS1PA1-PCB (Windows Environment)

- install SmartRF Flash programmer and CC debugger driver (admin rights necessary)

       >>> /devices/E18-MS1PA1-PCB/Flashing/flash-programmer-1.12.8.zip
       >>> /devices/E18-MS1PA1-PCB/Flashing/swrc212a.zip

- connect the debugger to the E18-MS1PA1-PCB 

       >>> /devices/E18-MS1PA1-PCB/Flashing/Programmer connection to E18-MS1PA1-PCB.png

       >>> CC debugger -> E18-MS1PA1-PCB

           1 -> GND
           2 -> 3,3V
           3 -> P2.2
           4 -> P2.1
           7 -> RESET
           9 -> 3,3V

           connect pin 2 and 9

- connect the CC debugger to the PC

- if the light on the CC debugger is RED

       >>> press set reset button on the CC debugger
       >>> if the light is still red, check the connection to the E18-MS1PA1-PCB   
       >>> GREEN light > ready for the next step   

- firewares 

       >>> /home/pi/miranda/devices/E18-MS1PA1-PCB/z-stack_firmware.zip
       >>> search for CC2530_CC2592

- start SmartRF Flash Programmer

       >>> select the new firmware (.hex file)
       >>> don't keep the old ieeeAddr
       >>> click “Perform actions” 

</br>

<a name="4.2 Raspberry Pi Connection"></a>

#### 4.2 Raspberry Pi Connection 

- Connect the E18-MS1PA1-PCB to the Raspberry

       >>> E18-MS1PA1-PCB -> Raspberry
	   
           VCC -> 3,3V (Pin1)
           GND -> GND  (Pin6)
           P02 -> TXD  (Pin8 / BCM 14)
           P03 -> RXD  (Pin10 / BCM 15)

</br>

<a name="4.3 Raspberry Pi Configuration"></a>

#### 4.3 Raspberry Pi Configuration 

- add following at the end of the config file

       >>> sudo nano /boot/config.txt 
	   
	         enable_uart=1
	         dtoverlay=pi3-disable-bt

- disable the modem system service 

       >>> sudo systemctl disable hciuart

- remove any of the following entries in the cmdline file, if present

       >>> sudo nano /boot/cmdline.txt

           console=serial0
           115200 console=ttyAMA0
           115200

- add the lines in zigbee2mqtt config

       >>> sudo nano data/configuration.yaml
	   
           serial:
             port: /dev/ttyAMA0
           advanced:
             baudrate: 115200
             rtscts: false

- reboot your raspberry	