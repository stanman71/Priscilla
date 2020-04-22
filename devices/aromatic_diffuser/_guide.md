# Aromatic Diffuser

This project provide customized aromatic diffuser modification.

   * <a href="#1 Hardware">1 Hardware</a>
      * <a href="#1.1 Aromatic Diffuser">1.1 Aromatic Diffuser</a>
      * <a href="#1.2 Controller">1.2 Controller</a>
      * <a href="#1.3 Sensor">1.3 Sensor</a>

</br>
------------
</br>

<a name="1 Hardware"></a>

### 1 Hardware

<a name="1.1 Aromatic Diffuser"></a>

#### 1.1 Aromatic Diffuser

- example

       >>> https://www.amazon.de/dp/B07X4F1JFB?ref_=pe_3044161_248799201_302_E_DDE_dt_1

</br>

<a name="1.2 Controller"></a>

#### 1.2 Controller

- Wemos D1 Mini v3

       >>> https://www.berrybase.de/raspberry-pi-co/esp8266-esp32/d1-mini-esp8266-entwicklungsboard

- resistor 3.3M

       >>> https://www.ebay.de/itm/10-Stuck-3-3-M-Ohm-1-4-Watt-5-Metalloxid-Widerstand-Widerstand/183455385692?hash=item2ab6cb085c:g:m-sAAOSwgbhaR5Ye

resistor 10K

       >>> https://www.berrybase.de/bauelemente/passive-bauelemente/widerstaende/metallschichtwiderstaende/0-6w-1/10k-953k-ohm/metallschichtwiderstand-10-0k-ohm-0-6w-177-1-0207-axial-durchsteckmontage?c=168

- resistor 220

       >>> https://www.ebay.de/itm/Widerstand-1Ohm-100-kOhm-Metallfilm-50-Stuck-Auswahl-1-4W-0-25W-1-Widerstande/372813822157?hash=item56cd6f78cd:m:mqtBKZoaux-2gebuzxM_WWg

- LED diode red / green

       >>> https://www.berrybase.de/bauelemente/aktive-bauelemente/leds/duo-blink-rgb-leds/kingbright-bi-color-indicator-led-5mm-rot/gr-252-n?c=139

- relais modul 

       >>> https://www.ebay.de/itm/5V-1-Channel-Relay-Shield-LED-for-Arduino-Relais-Modul-LED-fur-Arduino-CP0401B/281353504369?hash=item4181f9c671:g:wggAAOSwGL9eImVO

- voltage regulator

       >>> https://www.ebay.de/itm/3A-Mini-DC-DC-Spannungswandler-5V-23V-bis-3-3V-6V-9V-12V-FAP-HV/283696582512?hash=item420da24f70:g:hhkAAOSwvytcJeUX

- internal cables and connectors

       >>> https://www.berrybase.de/bauelemente/steckverbinder/rastersteckverbinder-2-50mm/kabel-mit-jst-xh-2.54mm-steckverbinder-awg26-20cm

- socket strip (2 pin)

       >>> https://www.berrybase.de/bauelemente/steckverbinder/stift-buchsenleisten-jumper/buchsenleiste-1x-2-polig-rm-2-54-h-8-4-gerade?c=114

- socket strip (3 pin)

       >>> https://www.berrybase.de/bauelemente/steckverbinder/stift-buchsenleisten-jumper/buchsenleiste-1x-3-polig-rm-2-54-h-8-4-gerade?c=114

</br>

<a name="1.3 Sensor"></a>

#### 1.3 Sensor

- Connect the sensor to the positive voltage of the aromatic diffuser fan (until 12V)
- Update the voltage values in aromatic_diffuser.ino (voltage_online + voltage_offline)