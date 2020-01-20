# Client Music - Complete Guide

A raspberry pi controller to play music by using spotify and lms. 

! This is the complete installation !

   * <a href="#1 Hardware">1 Hardware</a>
      * <a href="#1.1 Small Speaker (max 3W)">1.1 Small Speaker (max 3W)</a>
      * <a href="#1.2 Big Speaker (max 30W)">1.2 Big Speaker (max 30W)</a>        
   * <a href="#2 Prepare Raspian">2 Prepare Raspian</a>
   * <a href="#3 Comitup">3 Comitup</a>   
   * <a href="#4 Client Music">4 Client Music</a>
      * <a href="#4.1 Configuration">4.1 Configuration</a>
      * <a href="#4.2 Volume Control GUI">4.2 Volume Control GUI</a>      
      * <a href="#4.3 Volume Control Console">4.3 Volume Control Console</a>          
      * <a href="#4.4 Autostart">4.4 Autostart</a>
      * <a href="#4.5 Manually Control">4.5 Manually Control</a>
   * <a href="#5 Squeezelite Client">5 Squeezelite Client</a>
      * <a href="#5.1 Raspian">5.1 Raspian</a>
      * <a href="#5.2 Windows 10">5.2 Windows 10</a>
   * <a href="#6 Raspotify">6 Raspotify</a>
   * <a href="#7 Reduce Image size">7 Reduce Image size</a>   


</br>
------------
</br>

<a name="1 Hardware"></a>

### 1 Hardware

<a name="1.1 Small Speaker (max 3W)"></a>

#### 1.1 Small Speaker (max 3W)

- ! no direct sound control on the device !

- Raspberry Pi Zero WH

       >>> https://www.berrybase.de/raspberry-pi-zero-wh

- Micro SD-Card

       >>> https://www.amazon.de/dp/B073K14CVB/ref=twister_B073ZQ3L66?_encoding=UTF8&psc=1

- Hifiberry miniAMP

       >>> https://www.berrybase.de/raspberry-pi-co/raspberry-pi/erweiterungsboards/hifiberry/hifiberry-miniamp

- speaker + case

       >>> https://www.hs-sound.de/2-Stueck-Cheap-Trick-CT-209-Lautsprecher-Fertig-Gehaeuse-Holz-MDF-fuer-TangBand-W3-871_1

- power converter

       >>> https://www.ebay.de/itm/Auto-Ladeger-t-DC-Konverter-Modul-12V-5V-3A-15W-mit-Micro-USB-Kabel-New-UL-X/264570752052?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649

- power connector

       >>> https://www.berrybase.de/bauelemente/steckverbinder/stromversorgungs-steckverbinder/dc-stecker-hohlstecker/dc-einbaubuchse-f-252-r-hohlstecker-5-5x2-5mm-metallausf-252-hrung-l-246-tanschluss?c=115

- Power Source

       >>> https://www.amazon.de/LEICKE-Netzteil-Universal-2-5mm-Stecker/dp/B01I1JEWPU/ref=sr_1_15?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=netzteil%2BWS2811&qid=1571760422&sr=8-15&th=1

</br>

<a name="1.2 Big Speaker (max 30W)"></a>

#### 1.2 Big Speaker (max 30W)

- Raspberry Pi Zero WH

       >>> https://www.berrybase.de/raspberry-pi-zero-wh

- Micro SD-Card

       >>> https://www.amazon.de/dp/B073K14CVB/ref=twister_B073ZQ3L66?_encoding=UTF8&psc=1

- Hifiberry AMP2 

       >>> https://www.berrybase.de/raspberry-pi-co/raspberry-pi/erweiterungsboards/hifiberry/hifiberry-amp2

- Power Source

       >>> https://www.amazon.de/LEICKE-Netzteil-Universal-2-5mm-Stecker/dp/B07FLZ1SGY/ref=sr_1_15?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=netzteil%2BWS2811&qid=1571760422&sr=8-15&th=1

- Hifiberry Case

       >>> https://www.berrybase.de/raspberry-pi-co/raspberry-pi-zero/gehaeuse/geh-228-use-f-252-r-hifiberry-miniamp-und-raspberry-pi-zero-schwarz

- speaker example

       >>> https://www.hifisound.de/de/Hifi-Komponenten/Hifi-Lautsprecher/Kompakt/Q-Acoustics-3020i-Regal-Lautsprecher-weiss.html?gclid=EAIaIQobChMI3-zIouKK5wIVicx3Ch3hGQyGEAQYAiABEgIzc_D_BwE


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

- activate ssh on your raspberry pi

       >>> sudo raspi-config
       >>> Interfacing Options > SSH > Yes

- establish a network connetion

- open a remote connection 

       >>> Putty:

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
         
- create the new folder "smarthome" and copy all client_music files into it

       >>> mkdir smarthome

           FileZilla
   
           Protocol:   SFTP
           Server:     RaspberryPi IP-Address
           Port:       ---
           Connection: normal
           user:       pi
           password:   raspberry

- change folder permissions

       >>> sudo chmod -v -R 770 /home/pi/smarthome

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

       >>> sudo apt install /home/pi/smarthome/support/comitup_1.3.1-1_all.deb -y
       >>> sudo rm /etc/wpa_supplicant/wpa_supplicant.conf
       >>> sudo systemctl disable systemd-resolved
       >>> sudo systemctl stop systemd-resolved

- configuration

       >>> sudo nano /etc/comitup.conf

           replace ap_name and insert defaultclientmusic

- hotspot IP-Address:

       >>> 10.42.0.1 

- remove ssid-number

       >>> sudo rm /var/lib/comitup/comitup.json

- saved network connections  

       >>> cd /etc/NetworkManager/system-connections

- install folder 

       >>> /usr/share/comitup

</br>
------------
</br>  

<a name="4 Client Music"></a>

### 4 Client Music 

<a name="4.1 Configuration"></a>

#### 4.1 Configuration

- add hifiberry miniAMP config, if necessary

       >>> sudo nano /boot/config.txt    

           # hifiberry miniAMP
           dtoverlay=hifiberry-dac           

       >>> sudo reboot

- get audio card informations

       >>> cat /proc/asound/cards

- update config settings 

       >>> sudo nano /home/pi/smarthome/config.yaml

           insert your soundcard number 
 
           model names:
              - AMP2    > hifiberry_AMP2
              - miniAMP > hifiberry_miniAMP

</br>

<a name="4.2 Volume Control GUI"></a>

#### 4.2 Volume Control GUI

- open the alsamixer

       >>> alsamixer

           press "F6" and setect sound-device
           use arrow keys and change to "Digital" 

</br>

<a name="4.3 Volume Control Console"></a>

#### 4.3 Volume Control Console

https://blog.amnuts.com/2017/01/11/rotary-volume-control-for-the-raspberry-pi/
</br>
</br>

- get audio card informations

       >>> cat /proc/asound/cards

- search your soundcard and remenber the number
- get the commands overview

       >>> amixer -c [soundcard number] controls

- "Digital Playback Volume" has the number 1, get the setting overview

       >>> amixer cget -c [soundcard number] numid=1

- volume adjusting (example)

       >>> amixer -c [soundcard number] cset numid=1 175

</br>

<a name="4.4 Autostart"></a>

#### 4.4 Autostart

- create an autostart-file

       >>> sudo nano /etc/systemd/system/client_music.service

           [Unit]
           Description=Client Music
           After=network.target

           [Service]
           ExecStart=/home/pi/smarthome/client_music.py
           WorkingDirectory=/home/pi
           Restart=always

           [Install]
           WantedBy=multi-user.target

- enable autostart

       >>> sudo systemctl enable client_music.service

- start / stop service

       >>> sudo systemctl start client_music
       >>> sudo systemctl stop client_music

- show status / log

       >>> systemctl status client_music.service
       >>> journalctl -u client_music

</br>

##### ERROR: file not founded

http://www.server-wissen.de/linux-debian/ctrl-m-aus-einer-linux-datei-entfernen-m-entfernen/
</br>
</br>

- Open "client_music.py" in vi

       >>> vi /home/pi/smarthome/client_music.py

- remove ^M at the end of the first line (#!/usr/bin/python3)
- save changes (tipe :wq!)

</br>

<a name="4.5 Manually Control"></a>

#### 4.5 Manually Control 

- stop the client_music service

       >>> sudo systemctl stop client_music

- start the program manually

       >>> sudo python3 /home/pi/smarthome/client_music.py

- stop the program manually

       >>> sudo killall python3

</br>
------------
</br>

<a name="5 Squeezelite Client"></a>

### 5 Squeezelite Client

<a name="5.1 Raspian"></a>

#### 5.1 Raspian

https://forums.slimdevices.com/showthread.php?110523-squeezelite-shows-up-in-lms-settings-but-not-in-players
</br>
http://www.winko-erades.nl/installing-squeezelite-player-on-a-raspberry-pi-running-jessie/
</br>
</br>

- installation

       >>> sudo apt-get install squeezelite 

       or

       >>> sudo apt install /home/pi/smarthome/support/squeezelite_1.8-4.1+b1_armhf.deb -y

- get sound device informations

       >>> aplay -L

- squeezelite config (example)

       >>> sudo nano /etc/default/squeezelite 

           # ALSA output device:
	    SL_SOUNDCARD="hw:CARD=sndrpihifiberry,DEV=0 
	    SB_EXTRA_ARGS="-a 180"

- deactivate autostart

       >>> sudo systemctl disable squeezelite.service

- stop squeezelite 

       >>> sudo systemctl stop squeezelite      

- change hostname (equal to squeezelite name)

       >>> sudo nano /etc/hostname

</br>
    
<a name="5.2 Windows 10"></a>

#### 5.2 Windows 10

- installation

       >>> microsoft store >>> Squeezelite-X

</br>
------------
</br>

<a name="6 Raspotify"></a>

### 6 Raspotify (Spotify Connect Client for Raspian)

https://github.com/dtcooper/raspotify
</br>
https://dtcooper.github.io/raspotify/
</br>
</br>

- installation

       >>> curl -sL https://dtcooper.github.io/raspotify/install.sh | sh

       or

       >>> sudo apt install /home/pi/smarthome/support/raspotify-latest.deb

- get audio device informations

       >>> aplay -l
           (e.g "card 0, device 0" is "hw:0,0")
           
- raspotify config (example)

       >>> sudo nano /etc/default/raspotify

	    DEVICE_NAME=" ... " 
	    OPTIONS="--username <USERNAME> --password <PASSWORD> --device hw:0,1" 

- restart raspotify 

       >>> sudo systemctl restart raspotify
     
- deactivate autostart

       >>> sudo systemctl disable raspotify.service

- stop raspotify (program start choosed option)

       >>> sudo systemctl stop raspotify      

</br>
------------
</br>

<a name="7 Reduce Image size"></a>

- insert the cardreader with sd-card in a raspberry pi (raspian + gui)

- open a remote connection

- install GParted

       >>> sudo apt-get install gparted

- start GParted

       >>> Systemwerkzeuge / GParted   

- select the sd-card and reduce the partition size