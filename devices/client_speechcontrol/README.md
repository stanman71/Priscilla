# Client Speechcontrol

A raspberry pi controller to record voice. 

   * <a href="#1 Client Speechcontrol">1 Client Speechcontrol</a>
      * <a href="#1.1 Installation">1.1 Installation</a>
      * <a href="#1.2 Sound settings">1.2 Sound settings</a>      
      * <a href="#1.3 Test Sound settings">1.3 Test Sound settings</a>
      * <a href="#1.4 Replace alsa.conf">1.4 Replace alsa.conf</a>
      * <a href="#1.5 Create new Snowboy hotwords">1.5 Create new Snowboy hotwords</a>

</br>
------------
</br>

<a name="1 Client Speechcontrol"></a>

### 1 Client Speechcontrol

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

<a name="1.1 Installation"></a>

#### 1.1 Installation

- install dependencies

       >>> sudo apt -y install python-pyaudio python3-pyaudio sox python3-pip python-pip libatlas-base-dev

</br>

##### ERROR: Command 'arm-linux-gnueabihf-gcc' failed with exit status 1

- install portaudio first (https://github.com/jgarff/rpi_ws281x/issues/294)

       >>> sudo apt-get install portaudio19-dev

</br>

<a name="1.2 Sound settings"></a>

#### 1.2 Sound settings

- create ".asoundrc" in your home folder with correct hw settings (see example file in https://github.com/wanleg/snowboyPi or /devices/client_speechcontrol/Snowboy)

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

- find out hw cards (e.g "card 0, device 0" is "hw:0,0")

       >>> aplay -l
       >>> arecord -l

</br>

<a name="1.3 Test Sound settings"></a>

#### 1.3 Test Sound settings

- audio out

       >>> speaker-test -c 2

- record a 3 second clip 

       >>> arecord -d 3 test.wav

- verify

       >>> aplay test.wav

</br>

<a name="1.4 Replace alsa.conf"></a>

#### 1.4 Replace alsa.conf

       >>> sudo cp /home/pi/python/Snowboy/alsa.conf /usr/share/alsa/alsa.conf

           https://www.raspberrypi.org/forums/viewtopic.php?t=136974

</br>

##### ERROR: ImportError: dynamic module does not define module export function (PyInit__snowboydetect)
##### ERROR: No module named '_snowboydetect'

- create snowboydetect again (https://github.com/Kitt-AI/snowboy)

- install swig 

       https://github.com/Yadoms/yadoms/wiki/Build-on-RaspberryPI
       http://weegreenblobbie.com/?p=263

       >>> sudo apt-get install libpcre3-dev
       >>> wget http://prdownloads.sourceforge.net/swig/swig-3.0.12.tar.gz
       >>> tar xf swig-3.0.12.tar.gz
       >>> cd swig-3.0.12
       >>> ./configure --prefix=/usr
       >>> make -j 4
       >>> sudo make install
 
- check installed swig version

       >>> swig -version

- extract snowboy git archiv

       >>> unzip /home/pi/python/Snowboy/snowboy_1.3.0.zip -d /home/pi/snowboy

- create new detection files

       >>> cd /home/pi/snowboy/swig/Python3 
       >>> make

- replace "_snowboydetect.so" and "snowboydetect.py" in "/home/pi/python/app/speechcontrol/snowboy"

- delete the folder "/home/pi/snowboy"

</br>

##### ERROR: ALSA lib confmisc.c:1281:(snd_func_refer) Unable to find definition 'cards.bcm2835_alsa.pcm.front.0:CARD=0'

- if you got many ALBA errors like above and snowboy doesn't work reinstall raspian

</br>

<a name="1.5 Create new Snowboy hotwords"></a>

#### 1.5 Create new Snowboy hotwords

- log into https://snowboy.kitt.ai
- create a new hotword (try to find hotwords as different as possible)
- copy the downloaded file into the folder ~/resources/ on your raspberry pi
- add the new hotword and action in your system settings