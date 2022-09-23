# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# FEDERAL UNIVERSITY OF UBERLANDIA
# Faculty of Electrical Engineering
# Biomedical Engineering Lab
# ------------------------------------------------------------------------------
# Author: Italo Gustavo Sampaio Fernandes
# Contact: italogsfernandes@gmail.com
# Git: www.github.com/italogfernandes
# ------------------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------------------
import numpy as np
import math 
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Select dataset (comment in/out)

Fs = 10 # IMU sample rate
filePath = '0909test_2.csv'
#startTime = 2    # start to process from 1st second
#stopTime = 26
tempo_parado = 1 # keep still 3 seconds to average acc magnitude
mag_enabled = False

# -------------------------------------------------------------------------
# Import data

samplePeriod = 1/1000 # millis

dataset = pd.read_csv(filePath)
time = dataset.iloc[:,0].values * samplePeriod
accX = dataset.iloc[:,1].values
accY = dataset.iloc[:,2].values
accZ = dataset.iloc[:,3].values
gyrX = dataset.iloc[:,4].values
gyrY = dataset.iloc[:,5].values
gyrZ = dataset.iloc[:,6].values
yaw = dataset.iloc[:,7].values
pitch = dataset.iloc[:,8].values
roll = dataset.iloc[:,9].values
pid = dataset.iloc[:,10].values


# -------------------------------------------------------------------------
# Manually frame data
#indexSel1 = time > startTime
#indexSel2 = time < stopTime
#indexSel = indexSel1 * indexSel2

#time = time[indexSel]
#accX = accX[indexSel]
#accY = accY[indexSel]
#accZ = accZ[indexSel]
#gyrX = gyrX[indexSel]
#gyrY = gyrY[indexSel]
#gyrZ = gyrZ[indexSel]

# -------------------------------------------------------------------------
# Detect stationary periods

# Compute accelerometer magnitude
acc_mag = np.sqrt(accX**2 + accY**2 + accZ**2)
print("acc_mag length= ", len(acc_mag))
print("ACC-magnitude max= ", max(acc_mag))
print("ACC-magnitude min= ", min(acc_mag))

# HP filter accelerometer data
filtCutOff = 0.001
[b, a] = signal.butter(1, (2*filtCutOff)/(1/samplePeriod), 'high')
acc_magFilt = signal.filtfilt(b, a, acc_mag)

# Compute absolute value
acc_magFilt = abs(acc_magFilt)

# LP filter accelerometer data
filtCutOff = 5
[b, a] = signal.butter(1, (2*filtCutOff)/(1/samplePeriod), 'low')
acc_magFilt = signal.filtfilt(b, a, acc_magFilt)

# Descomente para ver a relação de tempo de espera para calibracao
# plt.plot(time, acc_magFilt)
# plt.plot(time[:(tempo_parado)*Fs], acc_magFilt[:(tempo_parado)*Fs])

# Threshold detection
stationaty_start_time = acc_magFilt[:(tempo_parado)*Fs]
statistical_stationary_threshold = np.mean(stationaty_start_time) + 7*np.std(stationaty_start_time)
#stationary_threshold = 0.048
stationary_threshold = statistical_stationary_threshold

print('Calculated Threshold = %f + 7 * %f = %f' % (np.mean(stationaty_start_time),
                                                     np.std(stationaty_start_time),
                                                     statistical_stationary_threshold))

print('Fixed Threshold = %f' % (stationary_threshold))

#stationary = acc_magFilt < stationary_threshold
stationary = acc_magFilt > stationary_threshold
print(stationary)
print(acc_magFilt)

# -------------------------------------------------------------------------
# Plot data raw sensor data and stationary periods
plt.figure(figsize=(20,10))
plt.suptitle('Sensor Data', fontsize=14)
ax1 = plt.subplot(2+mag_enabled,1,1)
plt.grid()
plt.plot(time, gyrX, 'r')
plt.plot(time, gyrY, 'g')
plt.plot(time, gyrZ, 'b')
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

## get quats
#quats = []
#for i in range(0, len(quat0)):
#    quats.append([quat0[i], quat1[i], quat2[i], quat3[i]])
#quats =np.array(quats)
#quat = quats

## -------------------------------------------------------------------------
## Compute translational accelerations
## rotate body accelerations to Earth frame
#import quaternion_toolbox
#a = np.array([accX, accY, accZ]).T
#acc = quaternion_toolbox.rotate(a, quaternion_toolbox.conjugate(quat))

acc = []
[acc.append([accX[i], accY[i], accZ[i]]) for i in range(len(accX))]
acc = np.array(acc)

# # Remove gravity from measurements
# acc = acc - [zeros(length(time), 2) ones(length(time), 1)]     # unnecessary due to velocity integral drift compensation

# Convert acceleration measurements to m/s/s
acc = acc * 9.81
acc[:,2] = acc[:,2] - 9.81
acc[:,2] = 0 # ignore accZ, set to 0

# Plot translational accelerations
plt.figure(figsize=(20,10))
plt.suptitle('Accelerations', fontsize=14)
plt.grid()

plt.plot(time, acc[:,0], 'r')
plt.plot(time, acc[:,1], 'g')
plt.plot(time, acc[:,2], 'b')
plt.title('Acceleration')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s/s)')
plt.legend(('X', 'Y', 'Z'))

# -------------------------------------------------------------------------
# Compute translational velocities


# Integrate acceleration to yield velocity
vel = np.zeros(np.shape(acc))
deltaT = np.zeros(np.shape(acc))
for t in range(1,len(deltaT)):
    deltaT[t] = time[t]-time[t-1]

for t in range(1,len(vel)):
    vel[t,:] = vel[t-1,:] + acc[t,:] * deltaT[t]
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

print('Error in Z: %.4f' % abs(pos[-1, 2]))

##-------------------------------------------------------------------------
## printout time, deltaT, velocity, position
#for t in range(1,len(deltaT)):
#    print(t, deltaT[t], vel[t,:], pos[t,:])

# -------------------------------------------------------------------------
#  Plot 3D foot trajectory

# # Remove stationary periods from data to plot
# posPlot = pos(find(~stationary), :)
# quatPlot = quat(find(~stationary), :)
posPlot = pos
#quatPlot = quat
plotlen = posPlot.shape[0] - 1
print("plot length = ", plotlen)

# Extend final sample to delay end of animation
extraTime = 20
onesVector = np.ones((extraTime*Fs, 1))
#TODO: usar pading
# np.pad()
#posPlot = np.append(arr = posPlot, values = onesVector * posPlot[-1, :])
#quatPlot = np.append(arr = quatPlot, values = onesVector * quatPlot[-1, :])

# -------------------------------------------------------------------------
# Create 6 DOF animation
# TODO: improve it

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

posPlot = posPlot.T

#
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

ax.set_xlim3d([-20.0, 20.0])
ax.set_ylim3d([-20.0, 20.0])
ax.set_zlim3d([-20.0, 20.0])

#
def update_lines(num):
    # NOTE: there is no .set_data() for 3 dim data...
    index = num*10
    line.set_data(posPlot[0:2, :index])
    line.set_3d_properties(posPlot[2,:index])
    return line

# Creating the Animation object
line_ani = animation.FuncAnimation(fig=fig, func=update_lines,
                                   frames = int(max(posPlot.shape)/10),
                                   fargs=None, 
                                   interval=50, blit=False)

plt.show()
