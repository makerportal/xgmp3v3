##############################################
#
# Calibrating Pressure Transducer XGMP3v3
# with Manual Manometer and Arduino
#
# by Joshua Hrisko, Maker Portal LLC (c) 2021
#
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
#
Volt_vals = (V_ref*np.divide(adc_vals,ADC_res-1.0)) # response of 24-bit XGMP3v3 in [mV]
P_vals   = (rho_2-rho_1)*g*np.array(h_vals)/(1000.0*1000.0) # pressure approx in [kPa]
#
# uncomment values below for test plot
# Volt_vals = np.array([0.77472656, 0.9580957 , 1.09505859, 1.23137695, 1.32902344,
#        1.41796875, 1.44697266, 1.57523437, 1.70800781, 1.84980469,
#        2.0109375 ])
# P_vals = np.array([-1.22888394, -0.87721604, -0.65546989, -0.36827444, -0.1856025 ,
#        -0.01953711,  0.04493534,  0.31845482,  0.60174285,  0.86940119,
#         1.194694  ])
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
l2, = ax.plot(Volt_vals,P_vals,color=plt.cm.Set1(0),linestyle='',marker='o',markersize=10,
              zorder=99,alpha=0.9)

ax.set_xlabel('XGMP3v3 Voltage, $V_R$ [V]',fontsize=16)
ax.set_ylabel('Manometer Pressure, $P$ [kPa]',fontsize=16)
ax.text(2.0, -1.5, 'Data Statistics:\n$R^2$      = '+'{0:2.2f}\nRMSE = {1:2.2f} kPa\n'.format(R_sq,rmse)+\
                    'PEFS = {0:2.2f}%\nMAE   = {1:2.2f} kPa\nBias   = {2:2.2f} kPa'.format(mape_span,mae,bias),
            size=16,ha="left", va="center",bbox=dict(boxstyle="round",
                       ec=(0.9, 0.9, 0.9),fc=(1.0, 1.0, 1.0),pad = 0.75))
# #
# ######################################################
# # Theory Comparison
# ######################################################
# #
# # directly from datasheet
t1, = ax.plot(V_span,P_theory,linewidth=4,color='k') # raw theory

# plotting error bounds
P_min = P_theory-(0.025*2.0*P_bound)
P_max = P_theory+(0.025*2.0*P_bound)
t2 = ax.plot(V_span,P_min,linestyle='--',color='k',alpha=0.5) # raw theory
t2 = ax.plot(V_span,P_max,linestyle='--',color='k',alpha=0.5) # raw theory
t2 = ax.fill_between(V_span,P_theory-(0.025*2.0*P_bound),P_theory+(0.025*2.0*P_bound),
                     color='#4b4b4b',alpha=0.5) # raw theory


# legend marking each line on the plot
ax.legend([l2,t1,t2],['Test Data','Theory','Full-Scale Error Bounds'],fontsize=16,bbox_to_anchor=(0,0,0.45,0.925))
fig.savefig('xgmp3v3_calibration_curve.png',dpi=300,bbox_inches='tight')
plt.show()
