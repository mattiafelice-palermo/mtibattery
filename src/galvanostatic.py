#!/usr/bin/env python

import sys
from io import StringIO

import numpy as np

class CellReadings(object):
    def __init__(self, filename):
        self.filename = filename
        self.cycles = []

        self._read_file(filename)

    def _read_file(self, filename):
        with open(filename,'r') as file:
            try:
                #--- Skip header
                for i in [1,2,3]:
                    line = file.readline()

                #--- Read cycle header
                line = file.readline()
                while True:
                    #--- Create cycle object
                    cycle = Cycle(line)
                    
                    #--- Read step header
                    line = file.readline()
                    
                    cycle_test = ''
                    
                    while cycle_test == '':
                        #--- Add step object to cycle
                        step_type = cycle.add_step(line)

                        #--- Read first record of current step
                        line = file.readline()
                        splitted = line.split('\t')
                        records = [] #contains all records of a step

                        #--- Reading records of a step
                        while splitted[1] == '':
                            records.append(line)
                            #--- Read next record and split it
                            line = file.readline()
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


class Cycle(object):
    def __init__(self, cycle_header):
        splitted_header = cycle_header.split('\t')
        self.cycle_id = splitted_header[0]
        self.steps = {}

    def __str__(self):
        return "Cycle_id: "+self.cycle_id
        #print("Cycle "+str(self.cycle_id))

    def add_step(self, step_header):
        step = Step(step_header, self.cycle_id)
        self.steps[step.type] = step
        return step.type

class Step(object):
    def __init__(self, step_header, parent_cycle_id):
        splitted_header = step_header.split('\t')
        self.parent_cycle_id = parent_cycle_id
        self.id = splitted_header[1]
        self.type = splitted_header[2]
        self.records = None

        self.datatype = np.dtype( [ ('none', np.str_), ('none2', np.str_),
                                    ('id', np.int), ('time', np.datetime64),
                                    ('voltage', np.float), ('current', np.float),
                                    ('temperature', np.float), ('capacity', np.float),
                                    ('specific_capacity', np.float), ('energy', np.float),
                                    ('specific_energy', np.float) ] ) #, ('realtime', np.datetime64) ] )

        self.dtype2 = np.dtype( [   ('voltage', np.float), ('current', np.float),
                                    ('temperature', np.float), ('capacity', np.float),
                                    ('specific_capacity', np.float), ('energy', np.float),
                                    ('specific_energy', np.float) ] ) #, ('realtime', np.datetime64) ] )

    def __str__(self):
        return "Step "+self.id+" type "+self.type+" of Cycle"+self.parent_cycle_id

    def add_records(self, record_list):
        rows = len(record_list)
        #m = np.fromiter(record_list[5:10],np.dtype([('col1', np.int)]))
        #m = np.loadtxt(StringIO(record_list[5:10]))

    
        
