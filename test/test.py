#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.abspath('../galvanostatic'))

from galvanostatic import CellReadings


filename='../data/20151123_CuHcF_3A_for_elettra.txt'
readings = CellReadings(filename)


#readings.plot_voltage_delta('CC_Chg')

print(readings.cycle_number)

#readings.cycles[1].plot_voltage(step='charge')
#readings.plot_efficiency(stride=10, mode='inverse')

print(readings.get_duration())
