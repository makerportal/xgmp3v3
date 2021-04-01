# XGMP3v3 Differential Pressure Sensor
XGMP3V3 Differential Pressure Sensor for Arduino and Raspberry Pi. This repository houses codes for approximating differential pressure from the XGMP3v3 sensor on an Arduino board or analog-to-digital converter (ADC) connected to a Raspberry Pi. Calibration codes are also given, which prints raw values from an Arduino board and reads the raw values into a Python program via the serial port. 

Get your XGMP3v3 Sensor: [XGMP3v3 Differential Pressure Sensor for Arduino and Raspberry Pi](https://makersportal.com/shop/xgmp3v3-differential-pressure-sensor-for-arduino-and-raspberry-pi) <br>
Follow along with the full tutorial: https://makersportal.com/

### JUMP TO:
<a href="#wiring">- Wiring Diagram</a><br>
<a href="#examples">- SSD1306 Examples with Pico</a><br>
<a href="#mapping">- Image Mapping with Python3</a><br>

The RPi Pico WS2812 library can be downloaded using git:

    git clone https://github.com/makerportal/rpi-pico-ssd1306

<a id="wiring"></a>
# - Wiring Diagram -

The wiring between the Pico and SSD1306 OLED is given below:
![SSD1306 RPi Pico Wiring](/images/ssd1306_w_RPi_Pico_white.jpg)
| Pico | SSD1306 |
| --- | --- |
| 3V3 (Pin 36) | VDD |
| GND (Pin 38) | GND | 
| I2C1_SDA (GP26) | SDA |
| I2C1_SCL (GP27) | SCK |
