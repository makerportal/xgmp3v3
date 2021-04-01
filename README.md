# XGMP3v3 Differential Pressure Sensor
XGMP3V3 Differential Pressure Sensor for Arduino and Raspberry Pi. This repository houses codes for approximating differential pressure from the XGMP3v3 sensor on an Arduino board or analog-to-digital converter (ADC) connected to a Raspberry Pi. Calibration codes are also given, which prints raw values from an Arduino board and reads the raw values into a Python program via the serial port. 

Get your XGMP3v3 Sensor: [XGMP3v3 Differential Pressure Sensor for Arduino and Raspberry Pi](https://makersportal.com/shop/xgmp3v3-differential-pressure-sensor-for-arduino-and-raspberry-pi) <br>
Follow along with the full tutorial: https://makersportal.com/

### JUMP TO:
<a href="#wiring">- Wiring Diagram</a><br>
<a href="#examples">- XGMP3v3 Example with an Arduino Uno Board</a><br>
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

<a id="examples"></a>
# - XGMP3v3 Example with an Arduino Uno Board -

The example code used to approximate differential pressure in [kPa] can be found at the code:

- xgmp3v3_main.ino 

The resulting output can be viewed from the serial port:

![XGMP3v3 Serial Output](/images/xgmp3v3_serial_ouptut.png)

<a id="calib"></a>
# - Calibration with Arduino and Python3 -

The XGMP3v3 can be calibrated using the two scripts contained within the 'calibration' folder. The first file (ending in .ino) needs to be uploaded to an Arduino board. The second file (.py) needs to be run on a computer with the Arduino board connected via USB. The following should be outputted as an example calibration plot:

![XGMP3v3 Calibration Curve](/images/xgmp3v3_calibration_curve.png)
