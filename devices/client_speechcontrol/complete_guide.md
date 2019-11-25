# Client Speechcontrol - Complete Guide

A raspberry pi controller for speech recognition based on snips.  

! This is the complete installation for a snips satellite!

   * <a href="#1 Hardware">1 Hardware</a>    
      * <a href="#1.1 Small Solution (2 Mics)">1.1 Small Solution (2 Mics)</a>   
      * <a href="#1.2 Big Solution (4 Mics)">1.2 Big Solution (4 Mics)</a>      
   * <a href="#2 Prepare Raspian">2 Prepare Raspian</a>
   * <a href="#3 Comitup">3 Comitup</a>   
   * <a href="#4 Snips.ai Satellites">4 Snips.ai Satellites</a>



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

- Respeaker 2 MIC HAT

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

- Respeaker 4 MIC ARRAY

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

- install pip

       >>> sudo apt-get install python3-pip -y

- install python modules

       >>> sudo pip3 install pyyaml 
       >>> sudo pip3 install paho-mqtt 
       >>> sudo pip3 install netifaces 
       >>> sudo pip3 install snipskit[hermes,mqtt]

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

- open hostname file and insert new name 

       >>> sudo nano /etc/hostname

- if your are using Respeaker 2MIC HAT install the driver

       >>> sudo apt-get install git
       >>> unzip /home/pi/python/support/seeed-voicecard.zip
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

<a name="4 Snips.ai Satellites"></a>

### 4 Snips.ai Satellites

https://docs.snips.ai/articles/platform/satellites
</br>
</br>


