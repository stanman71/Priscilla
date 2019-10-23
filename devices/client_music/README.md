# Client Music

A raspberry pi controller to play music by using spotify and lms. 

   * <a href="#1 Prepare Raspian">1 Prepare Raspian</a>
   * <a href="#2 Client Music">2 Client Music</a>
      * <a href="#2.1 Installation">2.1 Installation</a>
      * <a href="#2.2 Volume Control">2.2 Volume Control</a>      
      * <a href="#2.3 Autostart">2.3 Autostart</a>
      * <a href="#2.4 Manually Control">2.4 Manually Control</a>
   * <a href="#3 Comitup">3 Comitup</a>
   * <a href="#4 Squeezelite Client">4 Squeezelite Client</a>
      * <a href="#4.1 Raspian">4.1 Raspian</a>
      * <a href="#4.2 Windows 10">4.2 Windows 10</a>
   * <a href="#5 Raspotify">5 Raspotify</a>
   * <a href="#6 piCorePlayer & LMS">6 piCorePlayer & LMS</a>
      * <a href="#6.1 General Settings">6.1 General Settings</a>
      * <a href="#6.2 Squeezelite">6.2 Squeezelite</a>
      * <a href="#6.3 LMS">6.3 LMS</a>
      * <a href="#6.4 LMS Configuration">6.4 LMS Configuration</a>

</br>
------------
</br>

<a name="1 Prepare Raspian"></a>

### 1 Prepare Raspian 

- activate ssh

       >>> sudo raspi-config
       >>> Interfacing Options > SSH > Yes

       Putty Connection:

       Login IP
       Port 22
       User: pi
       Password: raspberry

- update raspian

       >>> sudo apt-get update && sudo apt-get upgrade

- install remote server

       >>> sudo apt-get purge realvnc-vnc-server

- enable VNC Server:

       >>> sudo raspi-config       

       Navigate to Interfacing Options
       Scroll down and select VNC 
       Yes

- install xrdp:

       >>> sudo apt-get install xrdp

- upgrade pip

       >>> pip install --upgrade pip

- open hostname file and insert new name (equal to squeezelite name)

       >>> sudo nano /etc/hostname
           
</br>
------------
</br>

<a name="2 Client Music"></a>

### 2 Client Music 

<a name="2.1 Installation"></a>

#### 2.1 Installation

- create the new folder "python" and copy all client_music files into it

       >>> mkdir python

       FileZilla

       Protocol:   SFTP
       Server:     RaspberryPi IP-Address
       Port:       ---
       Connection: normal
       user:       pi
       password:   raspberry

- change folder permissions

       >>> sudo chmod -v -R 070 /home/pi/python

- update config settings 

       >>> sudo nano /home/pi/python/config.yaml

</br>

<a name="2.2 Volume Control"></a>

#### 2.2 Volume Control

##### GUI

- open the alsamixer

       >>> alsamixer

           press "F6" and setect sound-device
           use arrow keys and change "Digital" 

##### Console

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

- volume adjusting 

       >>> amixer -c [soundcard number] cset numid=1 175

- insert your soundcard number in config.yaml

</br>

<a name="2.3 Autostart"></a>

#### 2.3 Autostart

- create an autostart-file

       >>> sudo nano /etc/systemd/system/client_music.service

           [Unit]
           Description=Client Music
           After=network.target

           [Service]
           ExecStart=/home/pi/python/client_music.py
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

       >>> vi /home/pi/python/client_music.py

- remove ^M at the end of the first line (#!/usr/bin/python3)
- save changes (tipe :wq!)

</br>

<a name="2.4 Manually Control"></a>

#### 2.4 Manually Control 

- stop the client_music service

       >>> sudo systemctl stop client_music

- start the program manually

       >>> sudo python3 /home/pi/python/client_music.py

- stop the program manually

       >>> sudo killall python3

</br>
------------
</br>

<a name="3 Comitup"></a>

### 3 Comitup (creates a Hotspot without wlan connection)

https://github.com/davesteele/comitup/wiki/Tutorial
</br>
https://packages.debian.org/sid/all/comitup/filelist
</br>
</br>

- installation steps:

       >>> sudo apt-get install comitup / sudo apt install /home/pi/python/support/comitup_1.3.1-1_all.deb
       >>> sudo rm /etc/wpa_supplicant/wpa_supplicant.conf
       >>> sudo systemctl disable systemd-resolved
       >>> sudo systemctl stop systemd-resolved
       >>> sudo touch /boot/ssh
       >>> sudo reboot

- LAN connected      > LAN-ADDRESS
- LAN not conneted   > 10.42.0.1 (Hotspot "comitup-")

- Connections folder > /etc/NetworkManager/system-connections
- Install folder     > /usr/share/comitup


</br>
------------
</br>  

<a name="4 Squeezelite Client"></a>

### 4 Squeezelite Client

<a name="4.1 Raspian"></a>

#### 4.1 Raspian

https://forums.slimdevices.com/showthread.php?110523-squeezelite-shows-up-in-lms-settings-but-not-in-players
</br>
http://www.winko-erades.nl/installing-squeezelite-player-on-a-raspberry-pi-running-jessie/
</br>
</br>

- installation

       >>> sudo apt-get install squeezelite / sudo apt install /home/pi/python/support/squeezelite_1.8-4.1+b1_armhf.deb

- get sound device informations

       >>> aplay -L

- squeezelite config

       >>> sudo nano /etc/default/squeezelite

	   SL_SOUNDCARD="hw:CARD=sndrpihifiberry,DEV=0"
	   SB_EXTRA_ARGS="-a 180"

- deactivate autostart

       >>> sudo systemctl disable squeezelite.service

- stop squeezelite (program start choosed option)

       >>> sudo systemctl stop squeezelite      

</br>
    
<a name="4.2 Windows 10"></a>

#### 4.2 Windows 10

- installation

       >>> microsoft store >>> Squeezelite-X

</br>
------------
</br>

<a name="5 Raspotify"></a>

### 5 Raspotify (Spotify Connect Client for Raspian)

https://github.com/dtcooper/raspotify
</br>
</br>

- installation

       >>> curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
       
- get audio device informations

       >>> aplay -l

- raspotify config

       >>> sudo nano /etc/default/raspotify

	   DEVICE_NAME=" ... " 
	   BITRATE="320"
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

<a name="6 piCorePlayer & LMS"></a>

### 6 piCorePlayer & LMS (Logitech Media Server)

https://www.picoreplayer.org/
</br>
https://www.basecube.de/2018/03/17/download/
</br>
</br>

<a name="6.1 General Settings"></a>

#### 6.1 General Settings

- change settings option to beta (options are at the bottom corner on the main site)

</br>

- wifi settings

       >>> activate wlan
       >>> insert wlan connetion data (ssid + password)

- main page

       >>> resize filesystem to 200mb
       >>> set a static ip-address

</br>

<a name="6.2 Squeezelite"></a>

#### 6.2 Squeezelite 

- create a multiroom group placeholder

       >>> activate squeezelite client on the server as multiroom group base
       >>> keep default settings (analog output)       
       >>> choose the player name "multiroom" (multiroom group name)       

- tweaks

       >>> activate squeezelite autostart

</br>

<a name="6.3 LMS"></a>

#### 6.3 LMS 

- installation

       >>> install LMS
       >>> start LMS  

- lms

       >>> activate lms autostart

</br>

<a name="6.4 LMS Configuration"></a>

#### 6.4 LMS Configuration (seperate WEB_GUI)

- IP-address

       >>> same as piCorePlayer, defaultport = 9000

- Logitech Account

       >>> not necessary, just skip it

- settings

       >>> plugins >>> install Spotty  

- config spotty

       >>> add premium account 
       >>> activate piCorePlayer "multiroom" at spotify connect only
       >>> activate option "Überwache die Verbindung der Spotty Connect Helferanwendung"       
       >>> multiroom group is now selectable in spotify

- synchronize players

       >>> set the player-groups on the main page in the upper-right corner 
           (Squeezelite must be installed and running on the clients)
       >>> synchronize all squeezelite clients with the multiroom group