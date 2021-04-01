//
// Arduino code used to read analog data from XGMP3v3 Differential Pressure
// Sensor and approximate airspeed in [m/s] using a pitot tube
// 
// by Joshua Hrisko, Maker Portal LLC (c) 2021
// 
//
int input_pin = A0;    // analog input pin
float V_ref = 3.3; // reference voltage
float ADC_res = pow(2.0,10); // ADC resolution (ATmega = 10-bit, SAMD21 = 12-bit)
float P_max =  0.5; // pressure max in [kPa] for specific XGMP3v3 sensor
float P_min = -0.5; // pressure min in [kPa] for specific XGMP3v3 sensor
float V_max = 2.7; // max analog voltage output
float V_min = 0.2; // min analog voltage output

float rho = 1.204; // air density

void setup() {
  analogReference(EXTERNAL); // set 3.3V as V_ref | not needed for SAMD21 boards
  Serial.begin(9600); // start serial 
  while (!Serial){}; // wait for serial to start (required for some boards)
}

void loop() {
  int adc_val; float volt_calc;  // sensor read variables
  float pres_approx;
  adc_val    = analogRead(input_pin); // read ADC data
  volt_calc  = (adc_val/(ADC_res-1.0))*V_ref; // convert ADC to voltage
  String prnt_str, str_buf; // string buffers for printing to serial port
  str_buf = "ADC val: ";
  prnt_str = str_buf+String(adc_val)+", Voltage: "; // adc value string
  str_buf = prnt_str + String(volt_calc,2)+" V, Pressure: "; // add voltage
  pres_approx = ((P_max-P_min)/(V_max-V_min))*(volt_calc-((V_max+V_min)/2.0));
  prnt_str = str_buf+String(pres_approx,2)+" kPa"; // add pressure approx [kPa]
//  Serial.println(prnt_str); // uncomment to print ADC, volt, and press to serial port

  float veloc; // velocity variable
  veloc = sqrt((2.0*(pres_approx*1000.0))/rho); // velocity approximation from pitot tube
  prnt_str = "Velocity: "+String(veloc,2)+" m/s"; // string for velocity printout
  Serial.println(prnt_str); // print velocity to serial port
  delay(50); // wait between readings for valid sensor reading [1ms]
}
