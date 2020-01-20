# Client Music - Image Guide

A raspberry pi controller to play music by using spotify and lms. 

! This manuell discribes the IMAGE based installation only !

   * <a href="#1 Hardware">1 Hardware</a>
      * <a href="#1.1 Small Speaker (max 3W)">1.1 Small Speaker (max 3W)</a>
      * <a href="#1.2 Big Speaker (max 30W)">1.2 Big Speaker (max 30W)</a>     
   * <a href="#2 Installation">2 Installation</a>
   * <a href="#3 Client Music">3 Client Music</a>
   * <a href="#4 Squeezelite Client">4 Squeezelite Client</a>
   * <a href="#5 Raspotify">5 Raspotify</a>

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

<a name="2 Installation"></a>

### 2 Installation 

- copy the image "client_music" on a sdcard

       >>> Win32DiskImager

- insert the card and start the raspberry pi

- search on your smartphone for a [defaultclientmusic-XX] network and connect

- open your browser and insert the following ip-address:

       >>> 10.42.0.1 

- select your wlan_ssid and insert your wlan_password

- open a remote connection to your raspberry pi  

       >>> Putty:

           Raspberry Pi IP-Address
           Port:     22
           User:     pi
           Password: raspberry

</br>
------------
</br>

<a name="3 Client Music"></a>

### 3 Client Music 

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
------------
</br>

<a name="4 Squeezelite Client"></a>

### 4 Squeezelite Client

- get sound device informations

       >>> aplay -L

- squeezelite config (example)

       >>> sudo nano /etc/default/squeezelite

           # ALSA output device:
	       SL_SOUNDCARD="hw:CARD=sndrpihifiberry,DEV=0"
	       SB_EXTRA_ARGS="-a 180"

- change hostname (equal to squeezelite name)

       >>> sudo nano /etc/hostname

</br>
------------
</br>

<a name="5 Raspotify"></a>

### 5 Raspotify (Spotify Connect Client for Raspian)

- get audio device informations

       >>> aplay -l
           (e.g "card 0, device 0" is "hw:0,0")

- raspotify config (example)

       >>> sudo nano /etc/default/raspotify

	    DEVICE_NAME=" ... " 
	    OPTIONS="--username <USERNAME> --password <PASSWORD> --device hw:1,0"

- restart the raspberry pi

       >>> sudo reboot