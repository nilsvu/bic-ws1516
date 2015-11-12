#!/usr/bin/env python2
# encoding: utf-8

import pyNN.nest as sim

def two_neuron_example(
        current=1000.0,
        time_simulation=2000.,
        weight=0.4,
        neuron_parameters={
            'v_rest'     : -65.0,
            'cm'         : 0.1,
            'tau_m'      : 1.0,
            'tau_refrac' : 2.0,
            'tau_syn_E'  : 10.0,
            'tau_syn_I'  : 10.0,
            'i_offset'   : 0.0,
            'v_reset'    : -65.0,
            'v_thresh'   : -50.0,
        },
    ):
    """
        Connects to neurons with corresponding parameters.

        The first is stimulated via current injection while the second receives
        the other one's spikes.
    """

    sim.setup(timestep=0.1, min_delay=0.1)

    pulse = sim.DCSource(amplitude=current, start=0.0, stop=time_simulation)

    pre = sim.Population(1, sim.IF_curr_exp(**neuron_parameters))
    post = sim.Population(1, sim.IF_curr_exp(**neuron_parameters))

    pre.record('spikes')
    post.record('spikes')

    sim.Projection(pre, post, connector=sim.OneToOneConnector(),
            synapse_type=sim.StaticSynapse(weight=weight),
            receptor_type='excitatory')

    pulse.inject_into(pre)

    sim.run(time_simulation)

    # rates in Hz
    rate_pre = len(pre.get_data('spikes').segments[0].spiketrains[0])\
            / time_simulation * 1000.

    rate_post = len(post.get_data('spikes').segments[0].spiketrains[0])\
            / time_simulation * 1000.

    sim.end()

    return rate_pre, rate_post
    
import matplotlib.pyplot as plt
import numpy as np
rate_pre = []
rate_post = []
current = []

for curr in np.linspace(0,500,1000):
	pre, post = two_neuron_example(current=curr)
	rate_pre.append(pre)
	rate_post.append(post)
	current.append(curr)

# Plot results
plt.figure(1)
plt.plot(current,rate_pre)
plt.xlabel('input current')
plt.ylabel('firing rate of first neuron [Hz]')
plt.savefig('figure1.png')

plt.figure(2)
plt.plot(rate_pre,rate_post)
plt.xlabel('firing rate of first neuron [Hz]')
plt.ylabel('firing rate of second neuron [Hz]')
plt.savefig('figure2.png')
