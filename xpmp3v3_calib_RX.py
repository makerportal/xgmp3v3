# # Calibrating Pressure Transducer XGZP6897A
# with Manual Manometer and Arduino
##############################################
#
#
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import serial,datetime,csv,os,time
import serial.tools.list_ports as COMs
#
#
############################################
# Find Arudino ports, select one,
# start communication with it
############################################
#
arduino_ports = [ii.device for ii in COMs.comports() if\
                 len((ii.device).split('ttyACM'))>1 or\
                 len((ii.device.split('ttyUSB')))>1 or\
                 len(ii.device.split('dev'))>1 and ii.manufacturer!=None]
ser = serial.Serial(arduino_ports[0],baudrate=9600) # match baud on Arduino
ser.flush() # clear the port

plt.style.use('ggplot')

def data_grabber():
    ser.write(b"data_req")
    time.sleep(0.1)
    ser_bytes = ser.read_all() # read Arduino serial data
    decoded_bytes = ser_bytes.decode('utf-8') # decode data to utf-8
    data = (decoded_bytes.replace('\r','')).replace('\n','')
    return data

def input_handler():
    while True: #broken by return
        try:
            input_str = input("Input New h Value from Manometer: ")
            return input_str
        except KeyboardInterrupt:
            return "exit"
######################################################
# Data Acquisition from Arduino and Write-in from
# manometer
######################################################
#
h_vals,adc_vals = [],[]
V_ref,ADC_res = 0.0,0.0
start_bool = False
while True:
    data = data_grabber()
    if start_bool==False and data.split(',')[0]=='Acquisition Start':
        # read the first line after acquisition start as header
        header = data.split(',')
        V_ref = float(header[1].split("=")[1])
        ADC_res = float(header[2].split("=")[1])
        start_bool = True
        print('Data Acquisition Starting...')
        continue
    if start_bool:
        h_input = input_handler()
        if h_input=="exit":
            print('Exiting Acquisition')
#             ser.close()
            break
        # saving data to variable to incrase speed
        # (saving to file happens after keyboard interrupt)
        pt_avg = []
        ser.flush()
        while len(pt_avg)<10:
            try:
                pt_avg.append(float(data_grabber()))
            except:
                break
        adc_vals.append(np.mean(pt_avg))
        h_vals.append(float(h_input))
        print('ADC val: {0:2.0f}, h: {1:2.1f}'.format(adc_vals[-1],h_vals[-1]))

#
######################################################
# Data and Conversion to Pressure/Voltage
######################################################
#
rho_2 = 997.0 # density of water [kg/m^3]
rho_1 = 1.225 # density of air [kg/m^3]
g   = 9.81 # gravity [m/s^2]
# h_vals   = np.divide([13.7,23.2,43.25,79.1,97.1,145.0,111.8,126.0,-17.4,-53.8,-95.2,-37.3,
#                      -73.6,-115.2,-146.2,-132.6],1000.0) # height of manometer under different pressures [mm]
# MPS_ADC_raw_vals = [9830572.0,9887678.0,10054668.0,10292554.0,10405446.0,
#                                  10726234.0,10497706.0,10608056.0,9601672.0,9351684.0,
#                                  9023918.0,9466900.0,9153698.0,8907830.0,8688792.0,8784272.0] # raw ADC vals
Volt_vals = (V_ref*np.divide(adc_vals,ADC_res)) # response of 24-bit XPMP3v3 in [mV]
P_vals   = (rho_2-rho_1)*g*np.array(h_vals)/(1000.0*1000.0) # pressure approx in [kPa]
#
######################################################
# Theory Approximations
######################################################
#
V_min = 0.2
V_max = 2.7
V_span = np.linspace(V_min,V_max,1000) # test voltages based on +25mV bias and 50mV full-scale claim
P_bound  = 2.5 # sensor Pressure boundary in +direction in [kPa]
P_sensitivity  = (2.0*P_bound)/(V_max-V_min)
P_intercept = -P_sensitivity*(((V_max-V_min)/2.0)+V_min)
P_theory = (P_sensitivity*V_span)+P_intercept
#
######################################################
# Theory Comparison Statistics
######################################################
#
P_predict = (P_sensitivity*Volt_vals) + P_intercept
rmse = np.sqrt(np.mean(np.power(np.subtract(P_predict,P_vals),2.0))) # root-mean square error
P_perc = 100.0*np.subtract(P_predict,P_vals)/P_vals
P_perc[P_perc==np.inf] = np.nan; P_perc[P_perc==-np.inf] = np.nan
mape = np.nanmean(np.abs(P_perc)) # mean absolute percent error
SS_tot = np.sum(np.power(P_vals-np.mean(P_vals),2.0))
SS_res = np.sum(np.power(P_vals-P_predict,2.0))
R_sq = 1.0-(SS_res/SS_tot) # coefficient of determination
mae  = np.mean(np.abs(np.subtract(P_predict,P_vals))) # mean absolute error
bias = np.mean(np.subtract(P_predict,P_vals))

P_perc_span = 100.0*np.subtract(P_predict,P_vals)/(2.0*P_bound)
P_perc_span[P_perc_span==np.inf] = np.nan; P_perc_span[P_perc_span==-np.inf] = np.nan
mape_span = np.nanmean(np.abs(P_perc_span)) # mean absolute percent error of span
#
######################################################
# Calibration Results
######################################################
#
fig,ax = plt.subplots(figsize=(14,8))
l2, = ax.plot(Volt_vals,P_vals,color=plt.cm.Set1(1),linestyle='',marker='o',markersize=10,zorder=99)

ax.set_xlabel('XPMP3v3 Voltage, $V_R$ [V]',fontsize=16)
ax.set_ylabel('Manometer Pressure, $P$ [kPa]',fontsize=16)
ax.text(2.0, -1.5, 'Data Statistics:\n$R^2$      = '+'{0:2.2f}\nRMSE = {1:2.2f} kPa\n'.format(R_sq,rmse)+\
                    'MAPE = {0:2.2f}%\nMAE   = {1:2.2f} kPa\nBias   = {2:2.2f} kPa'.format(mape,mae,bias),
            size=16,ha="left", va="center",bbox=dict(boxstyle="round",
                       ec=(0.9, 0.9, 0.9),fc=(1.0, 1.0, 1.0),pad = 0.75))
# #
# ######################################################
# # Theory Comparison
# ######################################################
# #
# # directly from datasheet
t1, = ax.plot(V_span,P_theory,linewidth=4,color=plt.cm.Set1(2)) # raw theory

# legend marking each line on the plot
ax.legend([l2,t1],['Data','Theory Prediction'],fontsize=16,bbox_to_anchor=(0,0,0.45,0.925))
plt.show()
