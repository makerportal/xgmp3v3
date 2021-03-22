/**
 * Code Used to send raw signal from XPMP3v3 Differential Pressure Sensor
 * to Python to be read against manometer for calibration
 * 
 * by Joshua Hrisko, Maker Portal LLC (c) 2021
 * 
 */

int input_pin = A0;    // analog input pin
float V_ref = 3.3; // reference voltage
float ADC_res = pow(2.0,10); // ADC resolution (ATmega = 10-bit, SAMD21 = 12-bit)
String in_comm = ""; // variable to handle data request command from Python

void setup() {
  analogReference(EXTERNAL); // set 3.3V as V_ref
  Serial.begin(9600); // start serial 
  while (!Serial){}; // wait for serial to start
  Serial.print("Acquisition Start,"); // start word for Python
  Serial.print("V_ref="); // V_ref
  Serial.print(V_ref); // send V_ref to Python
  Serial.print(",ADC_res="); // ADC resolution
  Serial.println(ADC_res); // send ADC resolution to Python
}

void loop() {
  int sensor_val; // sensor reading variable
  char in_char = Serial.read(); // read from serial
  if (in_char=='\r' or in_char=='\n' or int(in_char)==-1){
  } else {
    in_comm+=in_char; // save character from serial read
  }
  if (in_comm=="data_req"){ // listen for data request string
    sensor_val = analogRead(input_pin); // read analog data
    Serial.println(sensor_val); // send analog data to Python
    in_comm = ""; // reset comm. string to wait for wake word
  }
}
