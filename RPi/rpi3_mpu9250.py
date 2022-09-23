# ------------------------------------------------------------------------------
import sys
import numpy as np
import math 
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
# ------------------------------------------------------------------------------
# parameters
# -------------------------------------------------------------------------

Fs = 70 # IMU sample rate
filePath = 'mpu9250_2.csv'
beginTime  = 2  # the beginning of time to process data 
endTime    = 26 # the end of time to process data
stopPeriod = 3  # keep still 3 seconds to average acc magnitude
mag_enabled = False

# -------------------------------------------------------------------------
# Import data

samplePeriod = 1/1000 # millis

dataset = pd.read_csv(filePath)
time = dataset.iloc[:,0].values * samplePeriod
accX = dataset.iloc[:,1].values
accY = dataset.iloc[:,2].values
accZ = dataset.iloc[:,3].values
gyroX= dataset.iloc[:,4].values
gyroY= dataset.iloc[:,5].values
gyroZ= dataset.iloc[:,6].values
magX = dataset.iloc[:,7].values
magY = dataset.iloc[:,8].values
magZ = dataset.iloc[:,9].values
quat0= dataset.iloc[:,10].values
quat1= dataset.iloc[:,11].values
quat2= dataset.iloc[:,12].values
quat3= dataset.iloc[:,13].values

# -------------------------------------------------------------------------
# select data from beginTime to endTime 
# -------------------------------------------------------------------------
indexSel1 = time > beginTime
indexSel2 = time < endTime
indexSel = indexSel1 * indexSel2

time = time[indexSel]
gyroX= gyroX[indexSel]
gyroY= gyroY[indexSel]
gyroZ= gyroZ[indexSel]
accX = accX[indexSel]
accY = accY[indexSel]
accZ = accZ[indexSel]
magX = magX[indexSel]
magY = magY[indexSel]
magZ = magZ[indexSel]
quat0= quat0[indexSel]
quat1= quat1[indexSel]
quat2= quat2[indexSel]
quat3= quat3[indexSel]

# -------------------------------------------------------------------------
# Detect stationary data
# -------------------------------------------------------------------------
# Compute accelerometer magnitude
acc_mag = np.sqrt(accX**2 + accY**2 + accZ**2)
print("acc_mag length= ", len(acc_mag))

# Apply HighPass filter to accelerometer magnitude
filtCutOff = 0.001  
[b, a] = signal.butter(1, (2*filtCutOff) / Fs, 'high')
acc_magFilt = signal.filtfilt(b, a, acc_mag)

# Compute absolute value
acc_magFilt = abs(acc_magFilt)

# Apply LowPass filter to accelerometer magnitude
filtCutOff = 2
[b, a] = signal.butter(1, (2*filtCutOff)/ Fs, 'low')
acc_magFilt = signal.filtfilt(b, a, acc_magFilt)

# To see a filterred Acceleration magnitude in the stop period (for calibration)
# plt.plot(time, acc_magFilt)
# plt.plot(time[:stopPeriod*Fs], acc_magFilt[:stopPeriod*Fs])

# Threshold detection
stationaty_start_time = acc_magFilt[:stopPeriod*Fs]
statistical_stationary_threshold = np.mean(stationaty_start_time) + 2*np.std(stationaty_start_time)
stationary_threshold = statistical_stationary_threshold

print('Calculated Threshold = %f + 2 * %f = %f' % (np.mean(stationaty_start_time),
                                                     np.std(stationaty_start_time),
                                                     statistical_stationary_threshold))
print('Fixed Threshold = %f' % (stationary_threshold))

stationary = acc_magFilt < stationary_threshold

# -------------------------------------------------------------------------
# Plot data raw sensor data and stationary periods
# -------------------------------------------------------------------------
plt.figure(figsize=(20,10))
plt.suptitle('Sensor Data', fontsize=14)
ax1 = plt.subplot(2+mag_enabled,1,1)
plt.grid()
plt.plot(time, gyroX, 'r')
plt.plot(time, gyroY, 'g')
plt.plot(time, gyroZ, 'b')
plt.title('Gyroscope')
plt.ylabel('Angular velocity (º/s)')
plt.legend(labels=['X', 'Y', 'Z'])


plt.subplot(2+mag_enabled,1,2,sharex=ax1)
plt.grid()
plt.plot(time, accX, 'r')
plt.plot(time, accY, 'g')
plt.plot(time, accZ, 'b')
plt.plot(time, acc_magFilt, ':k')
plt.plot(time, stationary.astype(np.uint8)*acc_magFilt.max(), 'k', linewidth= 2)
plt.title('Accelerometer')
plt.ylabel('Acceleration (g)')
plt.legend(['X', 'Y', 'Z', 'Filtered', 'Stationary'])

if mag_enabled:
    plt.subplot(3,1,3,sharex=ax1)
    plt.grid()
    plt.plot(time, magX, 'r')
    plt.plot(time, magY, 'g')
    plt.plot(time, magZ, 'b')
    plt.title('Magnetrometer')
    plt.ylabel('Magnetic Flux Density  (G)')
    plt.legend(['X', 'Y', 'Z'])

plt.xlabel('Time (s)')

##-------------------------------------------------------------------------
## get quats for 3D rotation in Euler coordinates
##-------------------------------------------------------------------------
#quats = []
#for i in range(0, len(quat0)):
#    quats.append([quat0[i], quat1[i], quat2[i], quat3[i]])
#quats =np.array(quats)
#quat = quats

#-------------------------------------------------------------------------
# acceleration raw data
acc = []
[acc.append([accX[i], accY[i], accZ[i]]) for i in range(len(accX))]
acc = np.array(acc)

# Convert acceleration to m/s^2 (1g = 9.81 m/s^2)
acc = acc * 9.81
acc[:,2] = acc[:,2] - 9.81



#-------------------------------------------------------------------------
# gyroscope raw data
gyro = []
[gyro.append([gyroX[i], gyroY[i], gyroZ[i]]) for i in range(len(gyroX))]
gyro = np.array(gyro)

#-------------------------------------------------------------------------
# deltaT
deltaT = np.zeros(np.shape(acc))
for t in range(1,len(deltaT)):
    deltaT[t] = time[t]-time[t-1]
#-------------------------------------------------------------------------
# Kalman filter
#-------------------------------------------------------------------------
kalman = np.zeros(np.shape(acc))
Q=0.1;   
R=5;     
P00=0.1; 
P11=0.1; 
P01=0.1; 

for t in range(1,len(kalman)):	
    kalman[t,:] = kalman[t-1,:] - gyro[t,:] * deltaT[t]; # Kalman pitch
	
    P00 += deltaT[t] * (2 * P01 + deltaT[t] * P11); 
    P01 += deltaT[t] * P11; 
    P00 += deltaT[t] * Q;
    P11 += deltaT[t] * Q;
	
    Kk0 = P00 / (P00 + R);
    Kk1 = P01 / (P01 + R); 
	
    kalman[t,:] += (acc[t,:] - kalman[t-1,:]) * Kk0
	
    P00 *= (1 - Kk0);
    P01 *= (1 - Kk1);
    P11 -= Kk1 * P01;

# Plot filtered accelerations
plt.figure(figsize=(20,10))
plt.suptitle('Accelerations', fontsize=14)
plt.grid()

plt.plot(time, kalman[:,0], 'r')
plt.plot(time, kalman[:,1], 'g')
plt.plot(time, kalman[:,2], 'b')
plt.title('Kalman Acc')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s/s)')
plt.legend(('X', 'Y', 'Z'))

#-------------------------------------------------------------------------
# Integrate acceleration to yield velocity
vel = np.zeros(np.shape(acc))


for t in range(1,len(vel)):
    vel[t,:] = vel[t-1,:] + acc[t,:] * deltaT[t]
#    vel[t,:] = vel[t-1,:] + kalman[t,:] * deltaT[t]
    if stationary[t]:
        vel[t,:] = np.zeros((3))    # force zero velocity when foot stationary  

# Compute integral drift during non-stationary periods
velDrift = np.zeros(np.shape(vel))

d = np.append(arr = [0], values = np.diff(stationary.astype(np.int8)))
stationaryStart = np.where( d == -1)
stationaryEnd =  np.where( d == 1)
stationaryStart = np.array(stationaryStart)[0]
stationaryEnd = np.array(stationaryEnd)[0]


#for i in range(len(stationaryEnd)):
#    driftRate = vel[stationaryEnd[i]-1, :] / (stationaryEnd[i] - stationaryStart[i])
#    enum = np.arange(0, stationaryEnd[i] - stationaryStart[i])
#    enum_t = enum.reshape((1,len(enum)))
#    driftRate_t = driftRate.reshape((1,len(driftRate)))
#    drift = enum_t.T * driftRate_t
#    velDrift[stationaryStart[i]:stationaryEnd[i], :] = drift

# Remove integral drift
vel = vel - velDrift

# Plot translational velocity
plt.figure(figsize=(20,10))
plt.suptitle('Velocity', fontsize=14)
plt.grid()
plt.plot(time, vel[:,0], 'r')
plt.plot(time, vel[:,1], 'g')
plt.plot(time, vel[:,2], 'b')
plt.title('Velocity')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.legend(('X', 'Y', 'Z'))

# -------------------------------------------------------------------------
# Compute translational position

# Integrate velocity to yield position
pos = np.zeros(np.shape(vel))
for t in range(1,len(pos)):
    pos[t,:] = pos[t-1,:] + vel[t,:] * deltaT[t]   # integrate velocity to yield position

# Plot translational position
plt.figure(figsize=(20,10))
plt.suptitle('Position', fontsize=14)
plt.grid()
plt.plot(time, pos[:,0], 'r')
plt.plot(time, pos[:,1], 'g')
plt.plot(time, pos[:,2], 'b')
plt.title('Position')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.legend(('X', 'Y', 'Z'))

print('Error in Z: %f' % abs(pos[-1, 2]))

#-------------------------------------------------------------------------
#  Plot 3D Tracking
#-------------------------------------------------------------------------
posPlot = pos
#quatPlot = quat
plotlen = posPlot.shape[0] - 1
print("plot length = ", plotlen)


# Extend final sample to delay end of animation
extraTime = 20
onesVector = np.ones((extraTime*Fs, 1))
#TODO: user pading
# np.pad()
#posPlot = np.append(arr = posPlot, values = onesVector * posPlot[-1, :])
#quatPlot = np.append(arr = quatPlot, values = onesVector * quatPlot[-1, :])

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

posPlot = posPlot.T
print("posPlot shape = ",posPlot.shape)

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

data_x = posPlot[0,0:plotlen]
data_y = posPlot[1,0:plotlen]
data_z = posPlot[2,0:plotlen]

# Creating fifty line objects.
# NOTE: Can't pass empty arrays into 3d version of plot()
line = ax.plot(data_x, data_y, data_z)
line = line[0]

# Setting the axes properties
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_title('3D Animation')
ax.set_xlim3d([-1.0, 1.0]) # X-axis position render range (from -1 meter to 1 meter)
ax.set_ylim3d([-1.0, 1.0]) # X-axis position render range (from -1 meter to 1 meter)
ax.set_zlim3d([-1.0, 1.0]) # X-axis position render range (from -1 meter to 1 meter)

# update lines
def update_lines(num):
    # NOTE: there is no .set_data() for 3 dim data...
    index = num*10
    line.set_data(posPlot[0:2, :index])
    line.set_3d_properties(posPlot[2,:index])
    return line

print("frames = ", int(max(posPlot.shape)/10))

# Creating the Animation object
line_ani = animation.FuncAnimation(fig=fig, func=update_lines,
                                   frames = int(max(posPlot.shape)/10),
                                   fargs=None, 
                                   interval=50, blit=False)

plt.show()

