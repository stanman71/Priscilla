# Client Music - Configuration Guide

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

- Power Source

       >>> https://www.berrybase.de/raspberry-pi-co/raspberry-pi/stromversorgung/netzteile-fuer-die-steckdose/micro-usb-netzteil-5v/3-1a-schwarz

- Hifiberry Case

       >>> https://www.berrybase.de/raspberry-pi-co/raspberry-pi-zero/gehaeuse/geh-228-use-f-252-r-hifiberry-miniamp-und-raspberry-pi-zero-schwarz

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

       >>> https://www.berrybase.de/raspberry-pi-co/raspberry-pi/gehaeuse/fuer-raspberry-pi-3-modell-b/highpi-case-f-252-r-hifiberry-dac-43-rca/digi-43/amp-43-und-raspberry-pi-3-2-modell-b/

</br>
------------
</br>

<a name="2 Installation"></a>

### 2 Installation 

- copy the image "client_music" on a sdcard

       >>> Win32DiskImager

- insert the card and start the raspberry pi

- search on your smartphone for a [default_client_music_XX] network and connect

- open your browser and insert one of the following ip-addresses

       >>> if LAN is also connected      
           LAN-IP_ADDRESS

       >>> if LAN not conneted
           10.42.0.1 

- select your wlan_ssid and insert your wlan_password

- open a putty connection to your raspberry pi

       Login IP
       Port: 22
       User: pi
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

       >>> sudo nano /home/pi/python/config.yaml

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

- open hostname file and insert new name (equal to squeezelite name)

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