# Client Speechcontrol - Complete Guide

A raspberry pi controller for speech recognition based on snowboy. 

! This is the complete installation !

   * <a href="#1 Hardware">1 Hardware</a>    
      * <a href="#1.1 Small Solution (2 Mics)">1.1 Small Solution (2 Mics)</a>   
      * <a href="#1.2 Big Solution (4 Mics)">1.2 Big Solution (4 Mics)</a>      
   * <a href="#2 Prepare Raspian">2 Prepare Raspian</a>
   * <a href="#3 Comitup">3 Comitup</a>   
   * <a href="#4 Snips.ai">4 Snips.ai</a>
      * <a href="#4.1 Installation">4.1 Installation</a>   
      * <a href="#4.2 Snips Assistent">4.2 Snips Assistent</a>      
      * <a href="#4.3 Snips Kit">4.3 Snips Kit</a>    


</br>
------------
</br>

<a name="1 Hardware"></a>

### 1 Hardware

<a name="1.1 Small Solution (2 Mics)"></a>

#### 1.1 Small Solution (2 Mics)

- Raspberry Pi Zero WH

       >>> https://www.berrybase.de/raspberry-pi-zero-wh

- Micro SD-Card

       >>> https://www.amazon.de/dp/B073K14CVB/ref=twister_B073ZQ3L66?_encoding=UTF8&psc=1

- Respeaker 2 Mic Hat

       >>> https://www.berrybase.de/neu/respeaker-2-mics-hat-f-252-r-raspberry-pi

- Power Source

       >>> https://www.berrybase.de/raspberry-pi-co/raspberry-pi/stromversorgung/netzteile-fuer-die-steckdose/micro-usb-netzteil-5v/3-1a-schwarz



</br>

<a name="1.2 Big Solution (4 Mics)"></a>

#### 1.2 Big Solution (4 Mics)

- Raspberry Pi Zero WH

       >>> https://www.berrybase.de/raspberry-pi-zero-wh

- Micro SD-Card

       >>> https://www.amazon.de/dp/B073K14CVB/ref=twister_B073ZQ3L66?_encoding=UTF8&psc=1

- Respeaker 4 Mic Array

       >>> https://www.reichelt.de/respeaker-mic-array-v2-0-resp-mic-2-0-p248721.html?&trstct=pos_1

- Power Source

       >>> https://www.berrybase.de/raspberry-pi-co/raspberry-pi/stromversorgung/netzteile-fuer-die-steckdose/micro-usb-netzteil-5v/3-1a-schwarz



</br>
------------
</br>

<a name="2 Prepare Raspian"></a>

### 2 Prepare Raspian 

https://domoticproject.com/extending-life-raspberry-pi-sd-card/
</br>
https://www.antary.de/2018/12/28/raspberry-pi-ein-blick-auf-den-stromverbrauch/
</br>
https://scribles.net/disabling-bluetooth-on-raspberry-pi/
</br>
https://buyzero.de/blogs/news/raspberry-pi-strom-sparen-tipps-tricks
</br>
http://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT/
</br>
https://github.com/respeaker/mic_hat
</br>
https://github.com/respeaker/seeed-voicecard
</br>
</br>


- snips supported Raspbian Stretch only !

       >>> https://downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2019-04-09/

- activate ssh

       >>> sudo raspi-config
       >>> Interfacing Options > SSH > Yes

       Putty Connection:

       Login IP
       Port 22
       User: pi
       Password: raspberry

- update raspian

       >>> sudo apt-get update && sudo apt-get upgrade -y

- install pip

       >>> sudo apt-get install python3-pip -y

- install python modules

       >>> sudo pip3 install pyyaml 
       >>> sudo pip3 install paho-mqtt 
       >>> sudo pip3 install netifaces 
       >>> sudo pip3 install SpeechRecognition 

- disable swap        

       >>> sudo /sbin/dphys-swapfile swapoff

- minimise syslogging 

       >>> sudo nano /etc/rsyslog.conf

           deactivate all logging modules  

- remove bluetooth

       >>> sudo apt-get purge bluez -y
           sudo apt-get autoremove -y

- config power savings

       >>> sudo nano /boot/config.txt      

           # Disable HDMI
           disable_splash=1
           hdmi_blanking=1
           hdmi_ignore_hotplug=1
           hdmi_ignore_composite=1

           # Disable BLUETOOTH
           dtoverlay=pi3-disable-bt

           # Disable the ACT LED
           dtparam=act_led_trigger=none
           dtparam=act_led_activelow=off

           # Disable the PWR LED
           dtparam=pwr_led_trigger=none
           dtparam=pwr_led_activelow=off
         
- create the new folder "python" and copy all client_speechcontrol files into it

       >>> mkdir python

           FileZilla
   
           Protocol:   SFTP
           Server:     RaspberryPi IP-Address
           Port:       ---
           Connection: normal
           user:       pi
           password:   raspberry

- change folder permissions

       >>> sudo chmod -v -R 770 /home/pi/python

- install dependencies 

       >>> sudo apt-get install portaudio19-dev -y
       >>> sudo apt -y install python-pyaudio python3-pyaudio sox python3-pip python-pip libatlas-base-dev -y
       >>> sudo apt install python3-usb -y
       >>> sudo apt-get install libatlas-base-dev -y
       >>> sudo apt-get install python3-pyaudio -y

- open hostname file and insert new name 

       >>> sudo nano /etc/hostname

- if your are using Respeaker 2MIC HAT install the driver

       >>> sudo apt-get install git
       >>> git clone https://github.com/respeaker/seeed-voicecard.git
       >>> cd seeed-voicecard
       >>> sudo ./install.sh
       >>> sudo reboot

</br>
------------
</br>

<a name="3 Comitup"></a>

### 3 Comitup (creates a Hotspot without wlan connection)

https://davesteele.github.io/comitup/
</br>
https://packages.debian.org/sid/all/comitup/filelist
</br>
</br>

- installation steps:

       >>> sudo apt-get install comitup -y

       or
       
       >>> sudo apt install /home/pi/python/support/comitup_1.3.1-1_all.deb -y

       >>> sudo rm /etc/wpa_supplicant/wpa_supplicant.conf
       >>> sudo systemctl disable systemd-resolved
       >>> sudo systemctl stop systemd-resolved
       >>> sudo touch /boot/ssh
       >>> sudo reboot

- LAN connected      

       >>> LAN-ADDRESS

- LAN not conneted

       >>> 10.42.0.1 

- configuration

       >>> sudo nano /etc/comitup.conf

           replace ap_name and insert default_music_client

- remove ssid-number

       >>> sudo rm /var/lib/comitup/comitup.json

- saved network connections  

       >>> /etc/NetworkManager/system-connections

- install folder 

       >>> /usr/share/comitup

</br>
------------
</br>

<a name="4 Snips.ai"></a>

### 4 Snips.ai

https://console.snips.ai/login
</br>
https://smarthome-training.com/lokale-sprachsteuerung-mit-openhab-2-und-snips-ai/
</br>
https://docs.snips.ai/getting-started/quick-start-raspberry-pi
</br>
https://docs.snips.ai/articles/platform/satellites
</br>
</br>

<a name="4.1 Installation"></a>

#### 4.1 Installation

- install NodeJs and NPM

       >>> curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
       >>> sudo apt-get install -y nodejs
       >>> node -v -
       >>> npm -v

- install Snipes with SAM

       >>> sudo npm install -g snips-sam
       >>> sam connect raspberrypi.local
       >>> sam status
       >>> sam init

- setup audio devices

       >>> sam setup audio
       >>> sam test speaker
       >>> sam test microphone

- install mosquitto client
	
       >>> sam sound-feedback on

</br>

<a name="4.2 Snips Assistent"></a>

#### 4.2 Snips Assistent

- create an account on the website, if nessesary

       >>> https://console.snips.ai/signup

- login on the raspberry pi

       >>> sam login

- install the assistant with your new models

       >>> sam install assistant

- log output

       >>> sam watch

</br>

<a name="4.3 Snips Kit"></a>

#### 4.3 Snips Kit

- install snips kit

       >>> sudo pip3 install snipskit[hermes,mqtt]

