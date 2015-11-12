#!/usr/bin/env python2
# encoding: utf-8

    
import matplotlib.pyplot as plt
import numpy as np


#//***********************Constants
d = 2#; //dimensions
tSim = 200.#; //simulation time
Dt = 0.01#; //step size
windowStart = 77
windowEnd = 100
#//***********************Constants

#// use command: clear; g++ -std=c++11  main.cpp -o run; ./run

def HeavisideTheta(x = 0):
	if x > 0:
		return 1.
	elif x < 0:
		return 0.
	else:
		return 0.5
	
def spike(time, t0, amplitude):
	return amplitude*HeavisideTheta(time-(t0-0.5))*HeavisideTheta(-(time-(t0+0.5)))
		
def longInput(time, t0, t1, amplitude):
	return amplitude*HeavisideTheta(time-(t0))*HeavisideTheta(-(time-(t1)))
	
def slowRise(time, t0, t1, amplitude):
	return (time-t0)/(t1-t0)*longInput(time, t0, t1, amplitude)
	
def I_ext(time):
	#return spike(time, 60, 10) + slowRise(time, 80, 155, 15)
	#return longInput(time, 80,95, -10)
	#return spike(time, 80, 40)+spike(time, 85, 40)
	return spike(time, 80, 10)

print("\t\tDefining and Initialising") #############Defining and Initialising
timeList = []
	##################Hier die anfangsbedingung, abhängig von der dimension
timeList.append(0)
data_u = []
data_u.append(0.)#voltage
data_curr = []
data_curr.append(0)
##### get initial values of the gates -> s.t. they are in equilibrium
u = 0
a_n = (0.1-0.01 * u)/(np.exp(1.-0.1*u)-1.)
b_n = 0.125 * np.exp(-u/80.)
a_m = (2.5-0.1*u)/(np.exp(2.5-0.1*u)-1.)
b_m = 4.*np.exp(-u/18.)
a_h = 0.07 * np.exp(-u/20.)
b_h = 1./(np.exp(3.-0.1*u)+1.)

#### fill in values
data_m = []
data_m.append(a_m/(a_m+b_m))#m
data_n = []
data_n.append(a_n/(a_n+b_n))#n
data_h = []
data_h.append(a_h/(a_h+b_h))#h



E_Na = 115. #mV
E_K = -12. #mV
E_l = 10.6 #mV
g_Na = 120. #mS cm⁻2
g_K = 36.  #mS cm⁻2
g_l = 0.3 #mS cm⁻2
C_inv = 1.#/2.67 #pF^⁻1, aus 1.

print("\t\tIntegrating") #############Integrating
for step in np.arange(0,int(tSim/Dt)+2):
	time = Dt*step
	timeList.append(time)
	#print("--")
	#print(step)
	#print(time)
	###first excer
	#data0.append(data0[step]+Dt * 0.1 * (data0[step]+HeavisideTheta(time - 100.)))
	###second excer
	#data0.append(data0[step]+Dt * 0.1 * (data0[step]+HeavisideTheta(time - 100.)))
	###third exer
	#data0.append(data0[step]+Dt * (data1[step]))
	#data1.append(data1[step]-Dt * (data0[step]))
	###fourth excer
	u = data_u[step]
	m = data_m[step]
	n = data_n[step]
	h = data_h[step]
	I_l = g_l * (E_l-u)
	I_Na = g_Na*m*m*m*h*(E_Na-u)
	I_K = g_K*n*n*n*n*(E_K-u)
	data_u.append(u+C_inv * Dt *(I_l + I_Na + I_K +I_ext(time)))
	a_n = (0.1-0.01 * u)/(np.exp(1.-0.1*u)-1.)
	b_n = 0.125 * np.exp(-u/80.)
	a_m = (2.5-0.1*u)/(np.exp(2.5-0.1*u)-1.)
	b_m = 4.*np.exp(-u/18.)
	a_h = 0.07 * np.exp(-u/20.)
	b_h = 1./(np.exp(3.-0.1*u)+1.)
	data_n.append(n + Dt * (a_n + b_n) * ( a_n/(a_n+b_n) - n))
	data_m.append(m + Dt * (a_m + b_m) * ( a_m/(a_m+b_m) - m))
	data_h.append(h + Dt * (a_h + b_h) * ( a_h/(a_h+b_h) - h))
	data_curr.append(I_ext(time))
	
	#print(I_l, I_Na, I_K, I_ext(time), data0[0], data0[1])
	#print(data1[0], data2[0], data3[0])
	#print(data1[1], data2[1], data3[1])
	#exit()
	
	#if time > 100 and time < 130:
	#print(time, data0[step], HeavisideTheta(time-100.))

#print(timeList)
#print(data0)





print("\t\tShowing Data") #############Data
data_u = [x - 65. for x in data_u]# this is the voltage shift to get physiological values

# Plot results
#for i in range(0,d):
plt.figure(1)
fig, ax1 = plt.subplots()
ax1.plot(timeList, data_u)
ax2 = ax1.twinx()
ax2.plot(timeList, data_curr, 'r-')	
ax1.set_xlabel('time')
ax1.set_ylabel('voltage')
ax2.set_ylabel('ext current' , color='r')
ax1.set_xlim([windowStart,windowEnd])
ax2.set_xlim([windowStart,windowEnd])
#plt.ylim([-4,10])
plt.show()
#plt.savefig("figure1.png", dpi=72)



plt.figure(2)
plt.plot(timeList, data_m)
plt.plot(timeList, data_n)
plt.plot(timeList, data_h)
plt.xlim([windowStart,windowEnd])
plt.show()
#plt.xlabel('firing rate of first neuron [Hz]')
#plt.ylabel('firing rate of second neuron [Hz]')
#plt.savefig('figure2.png')
