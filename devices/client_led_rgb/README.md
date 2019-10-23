# Client LED_RGB

This project controls customized led stripes.

   * <a href="#1 Prepare Raspian">1 Prepare Raspian</a>
   * <a href="#2 Hardware">2 Hardware</a>
      * <a href="#2.1 LED Strip">2.1 LED Strip</a>
      * <a href="#2.2 Power Source">2.2 Power Source</a>


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

- open hostname file and insert new name

       >>> sudo nano /etc/hostname

</br>
------------
</br>

<a name="2 Hardware"></a>

### 2 Hardware

https://www.amazon.de/BTF-LIGHTING-Upgraded-Individually-Addressable-Waterproof/dp/B07DPHQWP8/ref=sr_1_2?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=WS2813B&qid=1570616287&sr=8-2&th=1
</br>
https://www.amazon.de/BTF-LIGHTING-WS2812B-300LEDs-Streifen-NichtWasserdicht/dp/B01CDTEJBG/ref=sr_1_2?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=WS2812B+LED+Streifen&qid=1569586703&s=diy&sr=1-2
</br>
https://www.reddit.com/r/arduino/comments/8g6yg3/led_strip_ws2812b_rgb_power_consumption/
</br>
https://www.pjrc.com/how-much-current-do-ws2812-neopixel-leds-really-use/
</br>
https://www.amazon.de/LEICKE-Netzteil-Universal-2-5mm-Stecker/dp/B01HRR9GY4/ref=sr_1_15?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=netzteil%2BWS2811&qid=1571760422&sr=8-15&th=1
</br>
https://www.amazon.de/LEICKE-Netzteil-Universal-2-5mm-Stecker/dp/B07YVBHH6K/ref=sr_1_15?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=netzteil+WS2811&qid=1571760422&sr=8-15
</br>
</br>

<a name="2.1 LED Strip"></a>

#### 2.1 LED Strip

- cheaper version without backup (all LEDs behind a broken LED are dark)

       >>> WS2812B 

- version with backup (all LEDs behind a broken LED running)

       >>> WS2813

<a name="2.2 Power Source"></a>

#### 2.2 Power Source

- 5V
- 60 mA per LED (white)

       >>> 30 LED / Meter > 1.8 A
       >>> 60 LED / Meter > 3.6 A      

- less power results in lower max brightness