# Client Speechcontrol - Complete Guide

A raspberry pi controller for speech recognition based on snowboy. 

! This is the complete installation !

   * <a href="#1 Hardware">1 Hardware</a>    
      * <a href="#1.1 Small Solution (2 Mics)">1.1 Small Solution (2 Mics)</a>   
      * <a href="#1.2 Big Solution (4 Mics)">1.2 Big Solution (4 Mics)</a>      
   * <a href="#2 Prepare Raspian">2 Prepare Raspian</a>
   * <a href="#3 Comitup">3 Comitup</a>   
   * <a href="#4 Client Speechcontrol">4 Client Speechcontrol</a>
      * <a href="#4.1 Configuration">4.1 Configuration</a>   
      * <a href="#4.2 Sound settings">2.2 Sound settings</a>      
      * <a href="#4.3 Test Sound settings">2.3 Test Sound settings</a>
      * <a href="#4.4 Replace alsa.conf">2.4 Replace alsa.conf</a>
      * <a href="#4.5 Autostart">4.5 Autostart</a>
      * <a href="#4.6 Manually Control">4.6 Manually Control</a>           
      * <a href="#4.7 Create new Snowboy hotwords">4.7 Create new Snowboy hotwords</a>

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
</br>

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

<a name="4 Client Speechcontrol"></a>

### 4 Client Speechcontrol

https://github.com/Kitt-AI/snowboy
</br>
https://github.com/wanleg/snowboyPi 
</br>
https://snowboy.kitt.ai
</br>
http://docs.kitt.ai/snowboy/
</br>
https://pimylifeup.com/raspberry-pi-snowboy/
</br>
</br>

<a name="4.1 Configuration"></a>

#### 4.1 Configuration

- update config settings 

       >>> sudo nano /home/pi/python/config.yaml

           model names:
              - Respeaker 2 Mic Hat   > respeaker_2mic           
              - Respeaker 4 Mic Array > respeaker_4mic

</br>

<a name="4.2 Sound settings"></a>

#### 4.2 Sound settings

- get hardware informations

       >>> aplay -l
       >>> arecord -l

           (e.g "card 0, device 0" is "hw:0,0")

- create ".asoundrc" in your home folder with your hardware informations 

       >>> sudo nano /home/pi/.asoundrc

           pcm.!default {
              type asym
              playback.pcm {
                type plug
                slave.pcm "hw:0,0"
              }
              capture.pcm {
                type plug
                slave.pcm "hw:1,0"
              }
           }

</br>

<a name="4.3 Test Sound settings"></a>

#### 4.3 Test Sound settings

- audio out

       >>> speaker-test -c 2

- record a 3 second clip 

       >>> arecord -d 3 test.wav

- verify

       >>> aplay test.wav

</br>

<a name="4.4 Replace alsa.conf"></a>

#### 4.4 Replace alsa.conf

       >>> sudo cp /home/pi/python/support/snowboy/alsa.conf /usr/share/alsa/alsa.conf

           https://www.raspberrypi.org/forums/viewtopic.php?t=136974

</br>

##### ERROR: ImportError: dynamic module does not define module export function (PyInit__snowboydetect)
##### ERROR: No module named '_snowboydetect'

- create snowboydetect again (https://github.com/Kitt-AI/snowboy)

- install swig 

       https://github.com/Yadoms/yadoms/wiki/Build-on-RaspberryPI
       http://weegreenblobbie.com/?p=263

       >>> sudo apt-get install libpcre3-dev -y
       >>> tar xf /home/pi/python/support/swig-3.0.12.tar.gz
       >>> cd swig-3.0.12
       >>> ./configure --prefix=/usr
       >>> make -j 4
       >>> sudo make install
 
- check installed swig version

       >>> swig -version

- extract snowboy git archiv

       >>> unzip /home/pi/python/support/snowboy_1.3.0.zip -d /home/pi/snowboy

- create new detection files

       >>> cd /home/pi/snowboy/swig/Python3 
       >>> make

- replace "_snowboydetect.so" and "snowboydetect.py" in "/home/pi/python/speechcontrol/snowboy"

- delete the folder "/home/pi/snowboy"

</br>

##### ERROR: ALSA lib confmisc.c:1281:(snd_func_refer) Unable to find definition 'cards.bcm2835_alsa.pcm.front.0:CARD=0'

- if you got many ALBA errors like above and snowboy doesn't work reinstall raspian

</br>

<a name="4.5 Autostart"></a>

#### 4.5 Autostart

- create an autostart-file

       >>> sudo nano /etc/systemd/system/client_speechcontrol.service

           [Unit]
           Description=Client Speechcontrol
           After=network.target

           [Service]
           ExecStart=/home/pi/python/client_speechcontrol.py
           WorkingDirectory=/home/pi
           Restart=always

           [Install]
           WantedBy=multi-user.target

- enable autostart

       >>> sudo systemctl enable client_speechcontrol.service

- start / stop service

       >>> sudo systemctl start client_speechcontrol
       >>> sudo systemctl stop client_speechcontrol

- show status / log

       >>> systemctl status client_speechcontrol.service
       >>> journalctl -u client_speechcontrol

</br>

##### ERROR: file not founded

http://www.server-wissen.de/linux-debian/ctrl-m-aus-einer-linux-datei-entfernen-m-entfernen/
</br>
</br>

- Open "client_speechcontrol.py" in vi

       >>> vi /home/pi/python/client_speechcontrol.py

- remove ^M at the end of the first line (#!/usr/bin/python3)
- save changes (tipe :wq!)

</br>

<a name="4.6 Manually Control"></a>

#### 4.6 Manually Control 

- stop the client_speechcontrol service

       >>> sudo systemctl stop client_speechcontrol

- start the program manually

       >>> sudo python3 /home/pi/python/client_speechcontrol.py

- stop the program manually

       >>> sudo killall python3

</br>

<a name="4.7 Create new Snowboy hotwords"></a>

#### 4.7 Create new Snowboy hotwords

- log into https://snowboy.kitt.ai
- create a new hotword (try to find hotwords as different as possible)
- copy the downloaded file into the folder ~/resources/ on your raspberry pi
- add the new hotword and action in your system settings

</br>
------------
</br>