#!/usr/bin/env python2
# encoding: utf-8

import pyNN.nest as sim
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def sim_neuron(rate):
	neuron_parameters={
            'v_rest'     : -50.0,
            'cm'         : 1,
            'tau_m'      : 20.0,
            'tau_syn_E'  : 5.0,
            'tau_syn_I'  : 5.0,
            'v_reset'    : -50.0,
            'v_thresh'   : 10000000000000000000000000000000000000000000000000000000000000000000000.0,
            'e_rev_E'	 : 0.0,
            'e_rev_I'	 : -100,
	}
	time_simulation = 100000 # don't choose to small number in order to get good statistics
	weight = 0.1 # is this value allreight
	sim.setup(timestep=0.1, min_delay=0.1)
	
	pois_exc = sim.SpikeSourcePoisson(duration=time_simulation,start=0.0,rate=rate) # generate poisson rate stimulus
	pois_inh = sim.SpikeSourcePoisson(duration=time_simulation,start=0.0,rate=rate) # generate poisson rate stimulus
	exc = sim.Population(1, cellclass=pois_exc) # simulate excitatory cell
	inh = sim.Population(1, cellclass=pois_inh) # simulate inhibitory cell
	
	rec = sim.Population(1, sim.IF_cond_exp(**neuron_parameters)) # simulate receiving neuron

	sim.Projection(exc, rec, connector=sim.OneToOneConnector(),synapse_type=sim.StaticSynapse(weight=weight),receptor_type='excitatory') # connect excitatory neuron to receiver
	sim.Projection(inh, rec, connector=sim.OneToOneConnector(),synapse_type=sim.StaticSynapse(weight=weight),receptor_type='inhibitory') # connect inhibitory neuron to receiver

	rec.record('v') # record membrane potential
	rec.record('gsyn_exc') # record excitatory conductance
	rec.record('gsyn_inh') # record inhibitory conductance
	sim.run(time_simulation) # start simulation

	return rec.get_data('v').segments[0].analogsignalarrays[0], rec.get_data('gsyn_exc').segments[0].analogsignalarrays[0], rec.get_data('gsyn_inh').segments[0].analogsignalarrays[0] # return membrane potential, excitatory conductance, inhibitory conductance

rate = 10000 # plug in solution of exercise b

pot, cond_exc, cond_inh = sim_neuron(rate) # apply function

tot_cond = cond_exc + cond_inh # calculate total conductance


hist, bin_edges = np.histogram(pot, density=True)
bin_centres = (bin_edges[:-1] + bin_edges[1:])/2

# Define model function to be used to fit to the data above:
def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))

# p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
p0 = [1., -50, 1.]



## PLOT MEMBRANE POTENTIAL DISTRIBUTION ##
plt.figure()
text = 'Membrane Potential Distribution'
hist, bins = np.histogram(pot,bins=1000, normed=True)
width = bins[1]-bins[0]
center = (bins[:-1] + bins[1:]) / 2.

coeff, var_matrix = curve_fit(gauss, center, hist, p0=p0)

# Get the fitted curve
hist_fit = gauss(center, *coeff)

plt.bar(center, hist, align='center', width=width, label=text, alpha=0.5, linewidth=0)
plt.plot(center, hist_fit,'r-', label='Fitted data')
plt.legend(bbox_to_anchor=(0.,1.02,1.,.0102),loc=3,ncol=1,mode="expand",borderaxespad=0.)
plt.xlabel('Potential $mV$')
plt.ylabel('norm. counts')
#plt.savefig(str(i) + '.png',bbox_inches='tight')
plt.show()

p0 = [1.,10,1.]

## PLOT MEMBRANE POTENTIAL DISTRIBUTION ##
plt.figure()
text = 'Membrane Potential Distribution'
hist, bins = np.histogram(tot_cond,bins=1000, normed=True)
width = bins[1]-bins[0]
center = (bins[:-1] + bins[1:]) / 2.

coeff, var_matrix = curve_fit(gauss, center, hist, p0=p0)

# Get the fitted curve
hist_fit = gauss(center, *coeff)

plt.bar(center, hist, align='center', width=width, label=text, alpha=0.5, linewidth=0)
plt.plot(center, hist_fit,'r-', label='Fitted data')
plt.legend(bbox_to_anchor=(0.,1.02,1.,.0102),loc=3,ncol=1,mode="expand",borderaxespad=0.)
plt.xlabel('Conductance $nS$')
plt.ylabel('norm. counts')
#plt.savefig(str(i) + '.png',bbox_inches='tight')
plt.show()

print(coeff)
print(var_matrix)
