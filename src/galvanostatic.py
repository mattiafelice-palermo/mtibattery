#!/usr/bin/env python
import sys
from io import StringIO

import numpy as np
import matplotlib.pyplot as plt

class CellReadings(object):
    def __init__(self, filename):
        self.filename = filename
        self.cycles = []

        self._read_file(filename)
        self.cycle_number = len(self.cycles)

    def _read_file(self, filename):
        with open(filename,'r') as data:
            try:
                #--- Skip header
                for i in [1,2,3]:
                    line = data.readline()

                #--- Read cycle header
                line = data.readline()
                while True:
                    #--- Create cycle object
                    cycle = Cycle(line)
                    
                    #--- Read step header
                    line = data.readline()
                    
                    cycle_test = ''
                    
                    while cycle_test == '':
                        #--- Add step object to cycle
                        step_type = cycle.add_step(line)

                        #--- Read first record of current step
                        line = data.readline()
                        splitted = line.split('\t')
                        records = [] #contains all records of a step

                        #--- Reading records of a step
                        while splitted[1] == '':
                            records.append(line[2:]) # remove two initial tabs
                            #--- Read next record and split it
                            line = data.readline()
                            splitted = line.split('\t')

                            #--- If EOF is reached, save data and raise except
                            if line == '':
                                cycle.steps[step_type].add_records(records)
                                self.cycles.append(cycle)
                                raise EOFError
                            
                        cycle.steps[step_type].add_records(records)
                        cycle_test = splitted[0]
                        
                    self.cycles.append(cycle)
            except EOFError:
                print("\nFinished reading file")
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

    def plot_voltage_delta(self, step_label):
        idx = []
        deltas = []
        for elem in self.cycles:
            idx.append(elem.cycle_id)
            deltas.append(elem.steps[step_label].voltage_delta)

        plt.scatter(idx,deltas)
        plt.plot(idx, deltas)
        plt.show()


class Cycle(object):
    def __init__(self, cycle_header):
        header = cycle_header.split('\t')
        self.cycle_id = header[0]
        self.steps = {}

    def __str__(self):
        return "Cycle_id: "+self.cycle_id

    def add_step(self, step_header):
        step = Step(step_header, self.cycle_id)
        self.steps[step.label] = step
        return step.label
        

class Step(object):
    def __init__(self, step_header, parent_cycle_id):
        header = step_header.split('\t')
        self.parent_cycle_id = parent_cycle_id
        self.step_id = int(header[1])
        self.label = header[2]
        self.time = header[3]
        self.capacity = float(header[4])
        self.specific_capacity = float(header[5])
        self.energy = float(header[6])
        self.specific_energy = float(header[7])
        self.capacitance = float(header[8])
        self.voltage_start = float(header[9])
        self.voltage_end = float(header[10])
        self.records = {}

        self.voltage_delta = self.voltage_end - self.voltage_start

    def __str__(self):
        return "Step "+str(self.step_id)+" type "+self.label+" of Cycle "+str(self.parent_cycle_id)

    def add_records(self, record_list):
        string = ''.join(record_list).replace(' ', 'T')
        csv = StringIO(string)
        self.records['id'], self.records['volt'] = np.loadtxt('data.dat', usecols=(0,2), unpack=True, dtype=[('id', np.int), ('volt', np.float)])

        # Using Pandas, slower
        #self.records = pd.read_csv(csv, header=None, index_col=False, delim_whitespace=True, names=col_head)
