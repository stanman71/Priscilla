# Client Speechcontrol - Complete Guide

A raspberry pi controller for speech recognition based on snips.  

! This is the complete installation for a snips satellite!

   * <a href="#1 Hardware">1 Hardware</a>    
      * <a href="#1.1 Small Solution (2 Mics)">1.1 Small Solution (2 Mics)</a>   
      * <a href="#1.2 Big Solution (4 Mics)">1.2 Big Solution (4 Mics)</a>      
   * <a href="#2 Prepare Raspian">2 Prepare Raspian</a>
   * <a href="#3 Comitup">3 Comitup</a>   
   * <a href="#4 Snips.ai Satellites">4 Snips.ai Satellites</a>
   * <a href="#5 Reduce Image size">5 Reduce Image size</a>   

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
         
- create the new folder "smarthome" and copy all client_speechcontrol files into it

       >>> mkdir smarthome

           FileZilla
   
           Protocol:   SFTP
           Server:     RaspberryPi IP-Address
           Port:       ---
           Connection: normal
           user:       pi
           password:   raspberry

- change hostname 

       >>> sudo nano /etc/hostname

- install respeaker driver

       >>> sudo apt-get install git -y
       >>> unzip /home/pi/smarthome/support/seeed-voicecard.zip
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
https://github.com/davesteele/comitup/wiki/Installing-Comitup
</br>
https://davesteele.github.io/comitup/archive.html
</br>
</br>

- installation steps:

       >>> sudo apt install /home/pi/smarthome/support/python3-networkmanager_2.0.1-4_all.deb
       >>> sudo apt install /home/pi/smarthome/support/comitup_1.3.1-1_all.deb -y
       >>> sudo rm /etc/wpa_supplicant/wpa_supplicant.conf
       >>> sudo systemctl disable systemd-resolved
       >>> sudo systemctl stop systemd-resolved

- hotspot IP-Address:

       >>> 10.42.0.1 

- edit configuration

       >>> sudo nano /etc/comitup.conf

           base_name: defaultclientspeechcontrol 

- remove ssid-number

       >>> sudo rm /var/lib/comitup/comitup.json

- saved network connections  

       >>> cd /etc/NetworkManager/system-connections

- install folder 

       >>> /usr/share/comitup

</br>
------------
</br>

<a name="4 Snips.ai Satellites"></a>

### 4 Snips.ai Satellites

https://docs.snips.ai/articles/platform/satellites
</br>
https://forum.creationx.de/forum/index.php?thread/1991-spracherkennung-ohne-cloud-mit-snips-und-raspberry-pi-teil-3-mit-satelliten-arbe/
</br>
https://forum.snips.ai/t/audio-server-reported-an-error-on-site-default-an-error-happened-while-trying-to-play-some-audio/3741/36
</br>
</br>

- update package informations

       >>> sudo apt-get install -y dirmngr
       >>> sudo bash -c 'echo "deb https://raspbian.snips.ai/$(lsb_release -cs) stable main" > /etc/apt/sources.list.d/snips.list'
       >>> sudo apt-key adv --fetch-keys  https://raspbian.snips.ai/531DD1A7B702B14D.pub
       >>> sudo apt-get update

- install NodeJs and NPM 

       >>> wget https://nodejs.org/dist/v10.17.0/node-v10.17.0-linux-armv6l.tar.gz
       >>> tar -xvf node-v10.17.0-linux-armv6l.tar.gz
       >>> cd node-v10.17.0-linux-armv6l
       >>> sudo cp -R * /usr/local/
       >>> node -v -
       >>> npm -v

- install satellite 

       >>> sudo apt install snips-hotword-model-heysnipsv4 -y
       >>> sudo apt install snips-satellite -y

- install SAM (Snips Assistant Manager)

       >>> sudo npm install -g snips-sam
       >>> sam connect [hostname].local 

- setup audio devices

       >>> sam setup audio
       >>> sam test speaker
       >>> sam test microphone

- edit settings
 
       >>> sudo nano /etc/snips.toml

           [snips-common]
           edit mqtt 
           edit mqtt_username             
           edit mqtt_password  

           [snips-audio-server]
           edit bind (e.g [hostname].local@mqtt)
           add portaudio_playback = "default" 

           [snips-hotword]       
           sensitivity = "0.25"
           
- restart raspberry pi

       >>> sudo reboot

</br>
------------
</br>

<a name="5 Reduce Image size"></a>

- insert the cardreader with sd-card in a raspberry pi (raspian + gui)

- open a remote connection

- install GParted

       >>> sudo apt-get install gparted

- start GParted

       >>> Systemwerkzeuge / GParted   

- select the sd-card and reduce the size