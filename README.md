# XGMP3v3 Differential Pressure Sensor
XGMP3V3 Differential Pressure Sensor for Arduino and Raspberry Pi. This repository houses codes for approximating differential pressure from the XGMP3v3 sensor on an Arduino board or analog-to-digital converter (ADC) connected to a Raspberry Pi. Calibration codes are also given, which prints raw values from an Arduino board and reads the raw values into a Python program via the serial port. 

Get your XGMP3v3 Sensor: [XGMP3v3 Differential Pressure Sensor for Arduino and Raspberry Pi](https://makersportal.com/shop/xgmp3v3-differential-pressure-sensor-for-arduino-and-raspberry-pi) <br>
Follow along with the full tutorial: https://makersportal.com/

### JUMP TO:
<a href="#wiring">- Wiring Diagram</a><br>
<a href="#examples">- XGMP3v3 Example with Arduino</a><br>
<a href="#calib">- Calibration with Arduino and Python3</a><br>

The XGMP3v3 library can be downloaded using git:

    git clone https://github.com/makerportal/xgmp3v3

<a id="wiring"></a>
# - Wiring Diagram -

The wiring between the XGMP3v3 and an Arduino Uno board is given below:
![XGMP3v3 Arduino Wiring](/images/xgmp3v3_sensor_wiring.jpeg)
| Arduino Uno | XGMP3v3 |
| --- | --- |
| 3V3 | VCC |
| GND | GND | 
| A0 | OUT |
