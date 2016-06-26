#!/usr/bin/env python
import sys
sys.path.append('/home/mattia/GitProjects/galvanostatic/src')

from galvanostatic import CellReadings


filename='20151126_graphite_foil_blank.txt'
filename='20151123_CuHcF_3A_for_elettra.txt'
readings = CellReadings(filename)


#readings.plot_voltage_delta('CC_Chg')

print(readings.cycle_number)

readings.cycles[1].plot_voltage(step='charge')
readings.plot_efficiency(stride=10, mode='inverse')
