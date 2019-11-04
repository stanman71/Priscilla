# Client LED_RGB

This project controls customized led stripes.

   * <a href="#1 Hardware">1 Hardware</a>
      * <a href="#1.1 LED Strip">1.1 LED Strip</a>
      * <a href="#1.2 Power Source">1.2 Power Source</a>
      * <a href="#1.3 Controller">1.3 Controller</a>

</br>
------------
</br>

<a name="1 Hardware"></a>

### 1 Hardware

<a name="1.1 LED Strip"></a>

https://www.youtube.com/watch?v=QnvircC22hU
</br>
http://www.thesmarthomehookup.com/the-complete-guide-to-selecting-individually-addressable-led-strips/
</br>
</br>

#### 1.1 LED Strip

https://de.aliexpress.com/item/32961181562.html?spm=a2g0x.12010612.8148356.2.17c34641klhRl2
</br>
https://www.amazon.de/UpgradeWS2812B-Individuell-Adressierbar-Wasserdicht-5M-WS2815-30-NP-BK-12V/dp/B07KXKF62H/ref=sr_1_4?keywords=VISDOLL&qid=1572691327&s=lighting&search-type=ss&sr=1-4
</br>
</br>

- specifications

       >>> WS2815 Chip
       >>> 12V
       >>> backup function (all LEDs behind a broken LED stay online)

</br>

<a name="1.2 Power Source"></a>

#### 1.2 Power Source

https://www.amazon.de/LEICKE-Netzteil-Universal-2-5mm-Stecker/dp/B07FLZ1SGY/ref=sr_1_15?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=netzteil%2BWS2811&qid=1571760422&sr=8-15&th=1
</br>
</br>

- 60 mA per LED (white)

       >>> 30 LED / Meter ~ 5  W
       >>> 60 LED / Meter ~ 10 W     

- less power results in lower max brightness

</br>

<a name="1.3 Controller"></a>

#### 1.3 Controller

- Wemos D1 Mini v3 (China only)

       >>> https://www.ebay.de/itm/WEMOS-D1-mini-ESP8266-4MB-V3-0-0-WIFI-Internet-of-Things-Based-Development-Board/273170891811

- voltage regulator L7805

       >>> https://www.ebay.de/itm/Spannungsstabilisator-STM-L7805CV-5V-L7812CV-12V-L7815CV-15V-1-5A-TO220-THT/153206933713

- capacitor 2200µF

       >>> https://www.ebay.de/itm/Elko-Panasonic-FR-2200uF-35V-Kondensator-105-C-Low-ESR-same-as-FM-854439/312606746499

- resistor 10K

       >>> https://www.ebay.de/itm/Kohleschicht-Widerstande-0-25W-5-Werte-und-Menge-WAHLBAR-5-10-50-100-Widerstand/221833069520

- relais

       >>> https://www.ebay.de/itm/1-Kanal-Relais-5V-230V-Raspberry-Pi-Modul-Channel-Relay-Arduino/252713915632

- internal cable connectors

       >>> https://www.ebay.de/itm/JST-XH-2-54-Stecker-inkl-15cm-Kabel-XH-Buchse-2-3-4-5-6-7-8-9-10-Pin-24AWG-RC/183748172867
       >>> https://www.ebay.de/itm/40p-10cm-Jumper-Wire-Steckbrucken-Steckbrett-Kabel-male-female-mannlich-wei/252795046460

- case

       >>> https://www.ebay.de/itm/Kunststoff-Gehause-Box-IP65-Modulgehause-Kunststoff-fur-elektronische-Bauteile/123699322855 (115 * 85 * 35)

- LED connector

       >>> https://www.ebay.de/itm/2-6-polig-M13-Steckverbinder-Paare-Kupplungen-Einbaustecker-5A-Metall/323694504483?hash=item4b5db22a23:m:m2bkEBP3zzAsnkZ22qxPWCw

- power connector

       >>> https://www.ebay.de/itm/Einbau-DC-Stecker-Buchse-Hohlsteckerbuchse-5-5-2-5-mm-Kupplung-Einbaubuchse-BL/333031450694