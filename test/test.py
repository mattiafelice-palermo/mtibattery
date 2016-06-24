#!/usr/bin/env python
import sys
sys.path.append('/home/mattia/GitProjects/galvanostatic/src')

from galvanostatic import CellReadings


filename='20151126_graphite_foil_blank.txt'

readings = CellReadings(filename)



print(readings.cycles[0].steps['CC_Chg'].time)

#readings.plot_voltage_delta('CC_Chg')

