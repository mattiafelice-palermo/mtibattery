#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.abspath('../mtibattery'))

from mtibattery import CellReadings


filename='../data/20151123_CuHcF_3A_for_elettra.txt'
filename='../data/20151126_graphite_foil_blank.txt'
filename='../../../angelo/20160621_AM15.txt'
readings = CellReadings(filename)


#readings.plot_voltage_delta('CC_Chg')

#print(readings.cycle_number)

#readings.cycles[1].plot_voltage(step='charge')
#readings.plot_efficiency(step=1)

#print(readings.get_duration())


#readings.plot_spcapacity(stride=50)

readings.save()
