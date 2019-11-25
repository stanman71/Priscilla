# Client LED_STRIP_CONTROLLER

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
       >>> backup function (all LEDs behind a broken LED still addressable)

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

       >>> https://www.berrybase.de/bauelemente/aktive-bauelemente/ics/ics-l../l7805abv-spannungsregler-linear-5v-1a-to-220-3-pin

- cooler TO-220

       >>> https://www.ebay.de/itm/5x-10x-TO220-Aluminium-Kuhlkorper-15x20mm-fur-Transistor-TO-220-Kuhler-Set/122909711162

- capacitor 2200µF

       >>> https://www.ebay.de/itm/Elko-Panasonic-FR-2200uF-35V-Kondensator-105-C-Low-ESR-same-as-FM-854439/312606746499

- capacitor 100µF

       >>> https://www.ebay.de/itm/10-Elko-Panasonic-FR-100uF-10V-Kondensator-105-C-Low-ESR-same-as-FM-856760/362414533288

- resistor 10K

       >>> https://www.berrybase.de/bauelemente/passive-bauelemente/widerstaende/metallschichtwiderstaende/0-6w-1/10k-953k-ohm/metallschichtwiderstand-10-0k-ohm-0-6w-177-1-0207-axial-durchsteckmontage?c=168

- resistor 330

       >>> https://www.berrybase.de/bauelemente/passive-bauelemente/widerstaende/metallschichtwiderstaende/0-6w-1/100-976-ohm/metallschichtwiderstand-330-0-ohm-0-6w-177-1-0207-axial-durchsteckmontage?c=168

- LED diode red / green

       >>> https://www.berrybase.de/bauelemente/aktive-bauelemente/leds/duo-blink-rgb-leds/kingbright-bi-color-indicator-led-5mm-rot/gr-252-n?c=139

- micro taster 

       >>> https://www.berrybase.de/bauelemente/schalter-taster/mikroschalter-taster/kurzhubtaster-vertikale-printmontage-6x6mm-h-5-0mm?c=86

- relais modul

       >>> https://www.berrybase.de/bauelemente/sensoren-module/relaiskarten/5v-1-kanal-relais-modul

- internal cables and connectors

       >>> https://www.ebay.de/itm/JST-XH-2-54-Stecker-inkl-15cm-Kabel-XH-Buchse-2-3-4-5-6-7-8-9-10-Pin-24AWG-RC/183748172867

- socket strip (2 pin)

       >>> https://www.berrybase.de/bauelemente/steckverbinder/stift-buchsenleisten-jumper/buchsenleiste-1x-2-polig-rm-2-54-h-8-4-gerade?c=114

- socket strip (3 pin)

       >>> https://www.berrybase.de/bauelemente/steckverbinder/stift-buchsenleisten-jumper/buchsenleiste-1x-3-polig-rm-2-54-h-8-4-gerade?c=114

- case (115 * 85 * 35)

       >>> https://www.ebay.de/itm/Kunststoff-Gehause-Box-IP65-Modulgehause-Kunststoff-fur-elektronische-Bauteile/123699322855 
           https://www.ebay.de/itm/Kunststoff-Gehause-Box-Platinen-Verteilerkasten-Elektronik-Netzteil-Montage-Neu/132994940466

- LED strip connector

       >>> https://www.ebay.de/itm/2-6-polig-M13-Steckverbinder-Paare-Kupplungen-Einbaustecker-5A-Metall/323694504483?hash=item4b5db22a23:m:m2bkEBP3zzAsnkZ22qxPWCw

- power connector

       >>> https://www.berrybase.de/bauelemente/steckverbinder/stromversorgungs-steckverbinder/dc-stecker-hohlstecker/dc-einbaubuchse-f-252-r-hohlstecker-5-5x2-5mm-metallausf-252-hrung-l-246-tanschluss?c=115