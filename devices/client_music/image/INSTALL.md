# Client Music IMAGE Installation

   * <a href="#1 Installation">1 Installation</a>
   * <a href="#2 Client Music">2 Client Music</a>
   * <a href="#3 Squeezelite Client">3 Squeezelite Client</a>
   * <a href="#4 Raspotify">4 Raspotify</a>

</br>
------------
</br>

<a name="1 Installation"></a>

### 1 Installation 

- copy the image on a sdcard

- insert the card an start the raspberry pi

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

<a name="2 Client Music"></a>

### 2 Client Music 

- get audio card informations

       >>> cat /proc/asound/cards

- update config settings 

       >>> sudo nano /home/pi/python/config.yaml

</br>
------------
</br>

<a name="3 Squeezelite Client"></a>

### 3 Squeezelite Client

- get sound device informations

       >>> aplay -L

- squeezelite config

       >>> sudo nano /etc/default/squeezelite

           # ALSA output device:
	       SL_SOUNDCARD="hw:CARD=sndrpihifiberry,DEV=0"
	       SB_EXTRA_ARGS="-a 180"

- open hostname file and insert new name (equal to squeezelite name)

       >>> sudo nano /etc/hostname

</br>
------------
</br>

<a name="4 Raspotify"></a>

### 4 Raspotify (Spotify Connect Client for Raspian)

- get audio device informations

       >>> aplay -l

- raspotify config

       >>> sudo nano /etc/default/raspotify

	       DEVICE_NAME=" ... " 
	       OPTIONS="--username <USERNAME> --password <PASSWORD> --device hw:1,0"

- restart the raspberry pi

       >>> sudo reboot