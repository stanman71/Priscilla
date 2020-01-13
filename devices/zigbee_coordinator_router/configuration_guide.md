# Zigbee Coordinator / Router

This project build a custom zigbee coordinator / router

   * <a href="#1 Coordinator">1 Coordinator</a>
      * <a href="#1.1 Hardware">1.1 Hardware</a>
      * <a href="#1.2 Flashing">1.2 Flashing</a>
      * <a href="#1.3 Raspberry Pi installation">1.3 Raspberry Pi installation</a>
   * <a href="#1 Router">1 Router</a>
      * <a href="#1.1 Hardware">1.1 Hardware</a>
      * <a href="#1.2 Flashing">1.2 Flashing</a>

</br>
------------
</br>

<a name="1 Coordinator"></a>

### 1 Coordinator

https://www.zigbee2mqtt.io/information/zigbee_network.html
</br>
https://ptvo.info/cc2530-based-zigbee-coordinator-and-router-112/
</br>
</br>

<a name="1.1 Hardware"></a>

#### 1.1 Hardware

- E18-MS1PA1-PCB

       >>> https://de.aliexpress.com/item/32803068018.html

- socket strip (2x5)

       >>> https://www.ebay.de/itm/273382759328?ViewItem=&item=273382759328

- internal cables and connectors

       >>> https://www.ebay.de/itm/JST-XH-2-54-Stecker-inkl-15cm-Kabel-XH-Buchse-2-3-4-5-6-7-8-9-10-Pin-24AWG-RC/183748172867

</br>

<a name="1.2 Flashing"></a>

https://github.com/Koenkk/Z-Stack-firmware
</br>
https://github.com/Koenkk/zigbee2mqtt/issues/1437
</br>
https://www.zigbee2mqtt.io/getting_started/flashing_the_cc2531.html
</br>
</br>

#### 1.2 Flashing (Windows Environment)

- install SmartRF Flash programmer and CC debugger driver (admin rights necessary)

       >>> /devices/zigbee_coordinator_router/Flashing/flash-programmer-1.12.8.zip
       >>> /devices/zigbee_coordinator_router/Flashing/swrc212a.zip

- connect the debugger to the E18-MS1PA1-PCB Board

       >>> CC debugger -> E18-MS1PA1-PCB

           1 -> GND
           2 -> 3,3V
           3 -> P2.2
           4 -> P2.1
           7 -> RESET
           9 -> 3,3V

           connect pin 2 and 9 of the debugger

<p align="center">
  <img src="https://github.com/stanman71/Watering_Control/blob/master/zigbee_coordinator/soldering/Flashing/Programmer%20connection%20to%20E18-MS1PA1-PCB.png">
</p>

</br>

- connect the CC debugger to the PC

- if the light on the CC debugger is RED

       >>> press set reset button on the CC debugger
       >>> if the light is still red, check the connection to the E18-MS1PA1-PCB 
       >>> check the solder joints on the PCB   

- if the light on the CC debugger is GREEN 

       >>> ready for the next step   

- unzip the firmware files

       >>> /home/pi/smarthome/devices/zigbee_coordinator_router/z-stack_firmware.zip

- start SmartRF Flash Programmer

       >>> select a coordinator firmware (.hex file) > default without router / source_routing with router
       >>> don't keep the old ieeeAddr
	>>> select "Erase, program and verify"
       >>> click “Perform actions” 

- if something fails, reset the CC debugger and restart the process

</br>

<a name="1.3 Raspberry Pi installation"></a>

#### 1.3 Raspberry Pi installation

https://www.zigbee2mqtt.io/information/connecting_cc2530.html
</br>
</br>

- connect the coordinator to the Raspberry Pi

       >>> coordinator -> Raspberry Pi
	   
                   VCC -> 3,3V (Pin1)
                   GND -> GND  (Pin6)
                   P02 -> TXD  (Pin8  / BCM 14)
                   P03 -> RXD  (Pin10 / BCM 15)

- start the Raspberry Pi

- add following at the end of the config file

       >>> sudo nano /boot/config.txt 
	   
           [zigbee]
           enable_uart=1
           dtoverlay=pi3-disable-bt

- disable the modem system service 

       >>> sudo systemctl disable hciuart

- remove any of the following entries in the cmdline file, if present

       >>> sudo nano /boot/cmdline.txt

           console=serial0,115200 
           console=ttyAMA0,115200

- add the lines in zigbee2mqtt config

       >>> sudo nano /opt/zigbee2mqtt/data/configuration.yaml
	   
           serial:
             port: /dev/ttyAMA0
           advanced:
             baudrate: 115200
             rtscts: false

- reboot your raspberry	

</br>
------------
</br>

<a name="2 Router"></a>

### 2 Router

https://www.zigbee2mqtt.io/information/zigbee_network.html
</br>
https://ptvo.info/cc2530-based-zigbee-coordinator-and-router-112/
</br>
</br>

<a name="2.1 Hardware"></a>

#### 2.1 Hardware

- E18-MS1PA1-PCB

       >>> https://de.aliexpress.com/item/32803068018.html

- socket strip (2x5)

       >>> https://www.ebay.de/itm/273382759328?ViewItem=&item=273382759328

- internal cables and connectors

       >>> https://www.ebay.de/itm/JST-XH-2-54-Stecker-inkl-15cm-Kabel-XH-Buchse-2-3-4-5-6-7-8-9-10-Pin-24AWG-RC/183748172867

- voltage regulator 3.3V 

       >>> https://www.ebay.de/itm/Dauerhafte-Qualitat-DC-DC-12V-zu-3-3V-5V-Step-Down-Netzteilmodul-A-O/362807517927?hash=item54790362e7:g:4ecAAOSwzWpZjrM5

- power connector 

       >>> https://www.berrybase.de/bauelemente/steckverbinder/stromversorgungs-steckverbinder/dc-stecker-hohlstecker/dc-einbaubuchse-f-252-r-hohlstecker-5-5x2-5mm-metallausf-252-hrung-l-246-tanschluss?c=115

- power source 

       >>> https://www.amazon.de/LEICKE-Netzteil-Universal-2-5mm-Stecker/dp/B01HRR96ZI/ref=sr_1_15?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=netzteil%2BWS2811&qid=1571760422&sr=8-15&th=1

- case

       >>> https://www.tme.eu/de/details/abs-54p/universal-gehause/maszczyk/km-54p-gy/
       >>> https://www.tme.eu/de/details/km-54p/universal-gehause/maszczyk/km-54p-bk/

</br>

<a name="2.2 Flashing"></a>

https://github.com/Koenkk/Z-Stack-firmware
</br>
https://github.com/Koenkk/zigbee2mqtt/issues/1437
</br>
https://www.zigbee2mqtt.io/how_tos/how_to_create_a_cc2530_router.html
</br>
</br>

#### 2.2 Flashing (Windows Environment)

- install SmartRF Flash programmer and CC debugger driver (admin rights necessary)

       >>> /devices/zigbee_coordinator_router/Flashing/flash-programmer-1.12.8.zip
       >>> /devices/zigbee_coordinator_router/Flashing/swrc212a.zip

- connect the debugger to the E18-MS1PA1-PCB Board

       >>> CC debugger -> E18-MS1PA1-PCB

           1 -> GND
           2 -> 3,3V
           3 -> P2.2
           4 -> P2.1
           7 -> RESET
           9 -> 3,3V

           connect pin 2 and 9 of the debugger

<p align="center">
  <img src="https://github.com/stanman71/Watering_Control/blob/master/zigbee_coordinator/soldering/Flashing/Programmer%20connection%20to%20E18-MS1PA1-PCB.png">
</p>

</br>

- connect the CC debugger to the PC

- if the light on the CC debugger is RED

       >>> press set reset button on the CC debugger
       >>> if the light is still red, check the connection to the E18-MS1PA1-PCB   
       >>> check the solder joints on the PCB  

- if the light on the CC debugger is GREEN 

       >>> ready for the next step   

- unzip the firmware files

       >>> /home/pi/smarthome/devices/zigbee_coordinator_router/z-stack_firmware.zip

- start SmartRF Flash Programmer

       >>> select a router firmware (.hex file)
       >>> don't keep the old ieeeAddr
	>>> select "Erase, program and verify"
       >>> click “Perform actions” 

- if something fails, reset the CC debugger and restart the process

- the coordinator needs a source_routing firmware in this case