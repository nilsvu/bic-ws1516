#!/usr/bin/env python2
# encoding: utf-8

import pyNN.nest as sim

def two_neuron_example(
        current=1000.0,
        time_simulation=2000.,
        weight=0.4,
        neuron_parameters={
            'v_rest'     : -50.0,
            'cm'         : 1,
            'tau_m'      : 20.0,
            'tau_refrac' : 5.0,
            'v_thresh'   : -40.0,
            'v_reset'	 : -50.0,
        },
    ):

    sim.setup(timestep=0.1, min_delay=0.1)

    pulse = sim.DCSource(amplitude=current, start=0.0, stop=time_simulation)

    pre = sim.Population(1, sim.IF_curr_exp(**neuron_parameters))

    pre.record('spikes')

    pulse.inject_into(pre)

    sim.run(time_simulation)

    # rates in Hz
    rate_pre = len(pre.get_data('spikes').segments[0].spiketrains[0])\
            / time_simulation * 1000.

    sim.end()

    return rate_pre
    
import matplotlib.pyplot as plt
import numpy as np
rate_pre = []
current = np.linspace(0.1,1000,500)

neuron_parameters={
            'v_rest'     : -50.0,
            'cm'         : 1,
            'tau_m'      : 20.0,
            'tau_refrac' : 5.0,
            'v_thresh'   : -40.0,
            'v_reset'	 : -50.0,
}

for curr in current:
	pre = two_neuron_example(current=curr,neuron_parameters=neuron_parameters)
	rate_pre.append(pre)

gl = neuron_parameters['cm']/neuron_parameters['tau_m']

nu = 1000/(neuron_parameters['tau_refrac']+neuron_parameters['tau_m']*np.log((neuron_parameters['v_reset']-neuron_parameters['v_rest']-current/gl)/(neuron_parameters['v_thresh']-neuron_parameters['v_rest']-current/gl)))
lim = 1000/(neuron_parameters['tau_refrac']) + current*0

# Plot results
plt.figure(1)
plt.plot(current,rate_pre,label='simulation')
plt.plot(current,nu,label='theory')
plt.plot(current,lim,'r-',label='theoretical limit')
plt.legend(loc=4)
plt.xlabel('input current')
plt.ylabel('firing rate of neuron [Hz]')
plt.ylim(0,250)
#plt.show()
plt.savefig('excercise2_5.png')
