#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:01:33 2019

@author: scott
"""

import numpy as np
from matplotlib import pyplot as plt

from EC_MS import download_cinfdata_set, plot_signal, plot_signal_vs_temperature, compare_signal_to_temperature
from EC_MS import load_calibration_results
from EC_MS import plot_flux

plt.close('all')


data = download_cinfdata_set(setup='microreactorNG', time='2019-06-25 09:52:30')

#plot_signal(data, leg=True, meta_data=['TC temperature'], rh_label='Temperature [C]')
#plot_signal_vs_temperature(data, leg=True, reciprocal=True)
compare_signal_to_temperature(MS_data=data)
plt.show()
exit()

mdict = load_calibration_results('19F04_calibration.pkl')



O2, CO2, CO, Ar = mdict['O2'], mdict['CO2'], mdict['CO'], mdict['Ar']

if True: # take background from CO2 cracking into account when calculating CO flux
    # NOTE below on why cal_mat is used exactly this way.
    CO.cal_mat = {'M28':1/CO.F_cal}
    CO.cal_mat['M44'] = - CO.cal_mat['M28'] * CO2.spectrum['M28']/CO2.spectrum['M44']



#plot_flux(data, mols=[O2, CO2, CO, Ar], unit='pmol/s')

CO2.get_bg(data, tspan=[0, 100])

tspan = [11000, 14000]
x, y = CO2.get_flux(data, tspan=tspan, background='preset',
                    unit='pmol/s')

fig, ax = plt.subplots()
ax.plot(x, y, color=CO2.get_color())
print(y.shape)
y_bg = CO2.background*1e12 * np.ones(y.shape)

ax.plot(x, y_bg, color=CO2.get_color(), linestyle='--')

ax.set_yscale('log')

ax.set_ylabel('cal. CO2 signal / [pmol/s]')
ax.set_xlabel('time / s')


print('CO2 flux during tspan=' + str(tspan) + ' is ' + str(np.mean(y)) + ' pmol/s')
#plt.show()


# Trying something else now !!!!


from EC_MS import Chip

chip = Chip('MR12')
print('\nAir flux through the chip in pmol/s: ' + str(chip.capillary_flow(gas='air') / 6.02e23 *  1e12))


print('flux of 1 bar CO2 through chip at 100 C in pmol/s: ' + str(chip.capillary_flow(gas='CO2', T=398.15) / 6.02e23 *  1e12))






x_CO2, y_CO2 = CO2.get_flux(data, tspan=[2000, 75000])
x_CO, y_CO = CO.get_flux(data, tspan=[2000, 75000])
x_Ar, y_Ar = Ar.get_flux(data, tspan=[2000, 75000])
x_O2, y_O2 = O2.get_flux(data, tspan=[2000, 75000])

l = min(len(y_CO2), len(y_CO), len(y_O2), len(y_Ar))


p_CO2 = y_CO2[0:l] / (y_CO2[0:l] + y_CO[0:l] + y_Ar[0:l] + y_O2[0:l]) # CO2 partial pressure in chip in bar
p_CO = y_CO[0:l] / (y_CO2[0:l] + y_CO[0:l] + y_Ar[0:l] + y_O2[0:l]) # CO2 partial pressure in chip in bar
p_Ar = y_Ar[0:l] / (y_CO2[0:l] + y_CO[0:l] + y_Ar[0:l] + y_O2[0:l]) # CO2 partial pressure in chip in bar
p_O2 = y_O2[0:l] / (y_CO2[0:l] + y_CO[0:l] + y_Ar[0:l] + y_O2[0:l]) # CO2 partial pressure in chip in bar

print(l)
t1 = 2500#end time of first cycle
t2 = 5000#end time of second cylle
t3 = 7500#end time of third cycle


fig, ax = plt.subplots()
ax.plot(x_CO2[0:l], p_CO2, color=CO2.get_color(), label='CO2')
ax.plot(x_CO2[0:l], p_CO, color=CO.get_color(), label='CO')
ax.plot(x_CO2[0:l], p_O2, color=O2.get_color(), label='O2')
ax.plot(x_CO2[0:l], p_Ar, color=Ar.get_color(), label='Ar')

ax.plot(x_CO2[0:t1], 0.5*np.ones(x_CO2[0:t1].shape), color='blue', linestyle='--')
ax.plot(x_CO2[t1:t2], 1/2.5*np.ones(x_CO2[t1:t2].shape),color='green', linestyle='--') 
ax.plot(x_CO2[t2:t3], 1/3.5*np.ones(x_CO2[t2:t3].shape), color='red', linestyle='--') 

plt.show()



'''
 ------- NOTE: use of m.cal_mat --------
When a Molecule object has the attribute cal_mat, it is used instead of the
more simple F_cal to calculate the molecule's flux from a given set of m/z signals.

Each m/z signal (at mass, e.g. 'M29') in the desired timespan is multiplied by cal_mat[M], and then
these are added up to give the flux. In the most simple case, cal_mat has only one
item, at the primary mass, which is just the reciprocal of F_cal (since F_cal is an absolute
sensitivity factor, you divide by it to go from signal to flux), i.e.:
molecule.cal_mat = {molecule.primary: 1/molecule.F_cal}

If we have an interference at the molecule's primary mass due to e.g., propane,
we can correct for this using cal_mat. We put a negative value for the primary mass
of the interfering molecule, i.e. 'M29' for propane, so that so that a factor times
the M29 signal is subtracted when calculating the flux. What should this factor be?
As an example, use propene, with primary='M41'. The signal at M41 is:

S_M41 = j_C3H6 * F_M41_C3H6 + j_C3H8 * F_M41_C3H8
S_M41 = j_C3H6 * F_M41_C3H6 + (S_M29/F_M29_C3H8) * F_M41_C3H8
isolating j_C3H6:
j_C3H6 = 1/F_M41_C3H6 * (S_M41 - F_M41_C3H8/F_M29_C3H8 * S_M29)
j_C3H6 = 1/F_M41_C3H6 * S_M41 + (-1/F_M41_C3H6 * F_M41_C3H8/F_M29_C3H8) * S_M29

so the factor to multiply S_M29 by, cal_mat['M29'] is
-1/F_M41_C3H6 * F_M41_C3H8/F_M29_C3H8  = -ratio/F_M41_C3H6

where ratio can be obtained from the propane spectrum:
ratio = C3H8.spectrum['M41']/C3H8.spectrum['M29']

This is implemented below.

'''

