#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:52:13 2019

@author: scott
"""

from matplotlib import pyplot as plt

from EC_MS import download_cinfdata_set, plot_signal, plot_flux
from EC_MS import Chip, point_calibration, recalibrate
from EC_MS import save_calibration_results

plt.close('all')


chip = Chip('SI-3iv1-14-B4')

print('\nAir flux through the chip in mol/s: ' + str(chip.capillary_flow(gas='air') / 6.02e23))


data = download_cinfdata_set(setup='microreactorNG', time='2019-02-22 14:05:27', use_caching=True)


ax = plot_signal(data, unit='A')
ax.legend()


O2 = point_calibration(data, mol='O2', mass='M32', cal_type='external', tspan=[2000, 3000], carrier='air', chip=chip)
Ar = point_calibration(data, mol='Ar', mass='M40', cal_type='external', tspan=[2000, 3000], carrier='air', chip=chip)
N2 = point_calibration(data, mol='N2', mass='M28', cal_type='external', tspan=[2000, 3000], carrier='air', chip=chip)

quantify = {'CH4':'M15', 'CO2':'M44', 'CO':'M28',
            #'CH3OH':'M31'
            }

def T(M):
    return M**(-1/2)

mdict, ax = recalibrate(quantify=quantify, trusted=[O2], external=[O2, Ar,
                        N2], transmission_function=T, labels=True)

CO2 = mdict['CO2']

plot_flux(data, mols=[O2, N2, Ar, CO2], tspan=[0, 3000], removebackground=False)

save_calibration_results(mdict, '19B22_calibration.pkl')
