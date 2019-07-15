#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:52:13 2019

@author: scott
"""

from matplotlib import pyplot as plt

from EC_MS import download_cinfdata_set, plot_signal
from EC_MS import chip_calibration, point_calibration, recalibrate
from EC_MS import load_calibration_results, save_calibration_results

plt.close('all')


mdict = load_calibration_results('19B22_calibration.pkl')

O2 = mdict['O2']

data = download_cinfdata_set(setup='microreactorNG', time='2019-06-04 17:29:26')

plot_signal(data, leg=True)


chip = chip_calibration(data, mol=O2, gas='O2', composition=1, chip='microreactor', tspan=[8200, 8350])

chip.save('MR12')

print('\nAir flux through the chip in mol/s: ' + str(chip.capillary_flow(gas='air') / 6.02e23))


Ar = point_calibration(data, mol='Ar', mass='M40', cal_type='external', tspan=[10000, 10200], carrier='Ar', chip=chip)
CO = point_calibration(data, mol='CO', mass='M28', cal_type='external', tspan=[15400, 15600], carrier='CO', chip=chip)
H2 = point_calibration(data, mol='H2', mass='M2', cal_type='external', tspan=[20000, 20200], carrier='H2', chip=chip)


def T(M):
    #return M**(-1/2)
    return M**(-1/2.5)


quantify = {'CH4':'M15', 'CO2':'M44', #'CO':'M28', # CO has an external calibration
            #'CH3OH':'M31' # we don't have a data file for methanol
            }

mdict, ax = recalibrate(quantify=quantify, trusted=[O2], external=[O2, Ar, H2, CO],
                            transmission_function=T, labels=True)


save_calibration_results(mdict, '19F04_calibration.pkl')



