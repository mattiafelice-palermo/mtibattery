"""This module allows the user to conveniently access the
   output of a MtiCorp Battery Analizer through a python
   interface and to run several computations and to plot/output
   the data.
"""

import sys
import os.path as path
from io import StringIO
import collections
import datetime as dt

import numpy as np
import matplotlib.pyplot as plt

from .helper import bstr2timedelta, str2timedelta


class CellReadings(object):
    """ Easy access to data from mticorp battery analyzer output.
    """

    def __init__(self, filename):
        """ Initialize a CellReadings object.
        The __init__ method initializes the object with filename
        and  empty lists for cycles. Invokes _read_file method
        to read the file and populate the CellReadings object.

        Parameters
        ----------
        filename : str
            Name of the input file
        """

        self.filename = filename  # name of the file
        self.cycles = []  # contains cycle objects
        self.headers = [] # contains column headers (probably useless...)

        # Call _read_file function to parse the input file
        self._read_file(filename)
        self.cycle_number = len(self.cycles)  # number of cycles

    def _read_file(self, filename):
        """ Read and parse input file.

        Parameters
        ----------
        filename : str
            Name of the input file

        Raises
        ------
        EOFError
            If end of file is reached.
        """
        with open(filename, 'r', encoding='utf-8') as data:
            try:
                #--- Skip first three lines of header
                self.headers = [data.readline() for i in range(3)]

                #--- Reads cycle header
                line = data.readline()  # cycle header
                while True:
                    #--- Create cycle object
                    cycle = Cycle(line)

                    #--- Read step header
                    line = data.readline()  # step header

                    # str: records always have a empty '' cycle entry
                    #      when a new cycle starts, cycle_test contains
                    #      the cycle number and thus the loops exits.
                    cycle_test = ''

                    while cycle_test == '':
                        #--- Add step object to cycle
                        # str: contains the step type (charge, discharge, rest)
                        step_type = cycle._add_step(line)

                        #--- Read first record of current step
                        line = data.readline()  # contains first step record
                        # split record line by tabs
                        splitted = line.split('\t')
                        records = []  # will contain all records of a step

                        #--- Read records of a step
                        while splitted[1] == '':  # splitted[1] is empty till a new
                                                 # step begins
                            # remove two initial empty fields
                            records.append(line[2:])
                            #--- Read next record and split it
                            line = data.readline()
                            splitted = line.split('\t')

                            #--- If EOF is reached, save data and raise except
                            #--- readline() returns '' when EOF is reached
                            if line == '':
                                cycle.steps[step_type]._add_records(records)
                                self.cycles.append(cycle)
                                raise EOFError

                        #--- Adds step to the cycle object
                        cycle.steps[step_type]._add_records(records)
                        cycle_test = splitted[0]

                    #--- Once all steps and records have been read and added
                    # to the cycle object, append the cycle object to
                    # self.cycles
                    self.cycles.append(cycle)
            except EOFError:
                print("\nFinished reading file")
            except:
                print("Unexpected error while reading file:",
                      sys.exc_info()[0])
                raise

    def get_duration(self):
        """ Returns total duration of the battery analysis.

        Returns
        -------
        dt.timedelta
            timedelta object containing total duration.

        """

        return np.sum([cycle.get_duration() for cycle in self.cycles])

    def save_cycles(self):
        output = []
        
        for cycle in self.cycles:
            output.append(list(cycle.properties.values()))

        root = path.splitext(path.basename(self.filename))[0]
        filename = root+".cycles.dat"
        header = ""
        np.savetxt(filename, np.vstack(output), fmt='%.5e', header=header) 

    def plot_voltage_delta(self, step_label):
        """ Plot difference between initial and final voltage of step type.

        The method plot_voltage_delta plots the difference between the initial
        and the final voltage of a given step type as a function of the cycle
        number.

        Parameters
        ----------
        step_label : str  {'Rest', 'CC_Charge', 'CC_DChg'}
            Contains step type.
        """

        idx = []  # cycle indices
        deltas = []  # delta voltages

        #--- Cycle over each cycle
        for elem in self.cycles:
            idx.append(elem.cycle_id)
            deltas.append(elem.steps[step_label].voltage_delta)

        #--- Plot data with matplotlib
        plt.scatter(idx, deltas)
        plt.plot(idx, deltas)
        plt.show()

    def plot_voltage(self, start=0, stop=None, step=1):
        """ Plot voltage as a function of the record index.

        Parameters
        ----------
        start : int
            First cycle to plot
        stop : int
            Last cycle to plot
        step : int
            Read every 'step's cycles.
        """

        idx = []  # record indexes
        voltages = []

        #--- Cycle over each cycle
        for cycle in self.cycles[start:stop:step]:
            for step in cycle.steps.values():
                idx.extend(step.records['id'])
                voltages.extend(step.records['volt'])

        #--- Plot data with matplotlib
        plt.plot(idx, voltages)
        plt.show()

    def plot_spcapacity(self, start=0, stop=None, step=1):
        """ Plot specific capacity as a function of the voltage.

        Parameters
        ----------
        start : int
            First cycle to plot
        stop : int
            Last cycle to plot
        step : int
            Read every 'step's cycles.
        """
        #--- Cycle over each cycle
        for cycle in self.cycles[start:stop:step]:
            for step in cycle.steps.values():
                if step.label == 'CC_Chg':
                    # Charge voltage is plotted in red
                    plt.plot(step.records['volt'],
                             step.records['sp_capacity'], 'r')
                elif step.label == 'CC_DChg':
                    # Discharge voltage is plotted in blue
                    plt.plot(step.records['volt'],
                             step.records['sp_capacity'], 'b')
                else:
                    # Rest voltage is plotted in black
                    plt.plot(step.records['volt'],
                             step.records['sp_capacity'], 'k')

        #--- Show the plot
        plt.show()

    def plot_efficiency(self, start=0, stop=None, step=1, mode='standard'):
        """ Plot battery efficiency as a function of the cycle number.

        Parameters
        ----------
        start : int
            First cycle to plot
        stop : int
            Last cycle to plot
        step : int
            Read every 'step's cycles.
        mode : str {'standard', 'inverse'}
            Choose whether to compute discharge/charge (standard) or inverse.

        Notes
        -----
        The efficiency of a cycle is computed as the ratio between the discharge
        and charge time. If mode is set to 'inverse', then it is computes as
        the ratio between the charge and discharge time.
        """
        idx = []  # cycle indices
        efficiency = []

        # Cycle over cycles
        for cycle in self.cycles[start:stop:step]:
            idx.append(cycle.cycle_id)
            efficiency.append(cycle.get_efficiency(mode))

        #--- Plot with matplotlib
        plt.scatter(idx, efficiency)
        plt.plot(idx, efficiency)
        plt.show()


class Cycle(object):
    """ Contains information of a (rest)-charge-discharge cycle.
    """

    head_entries = [('cycle_id', int), ('charge_capacity', float),
                    ('discharge_capacity', float), ('charge_capacity_sp', float),
                    ('discharge_capacity_sp', float), ('efficiency', float),
                    ('charge_energy', float), ('discharge_energy', float),
                    ('midval_voltage', float), ('charge_capacity2', float),
                    ('charge_ratio', float), ('platform_capacity', float),
                    ('platform_capacity_sp', float),
                    ('platform_efficiency', lambda x: float(x.split('#')[0])),
                    ('platform_duration', str2timedelta),
                    ('charge_capacitance', float),
                    ('discharge_capacicance', float), ('rd', float),
                    ('charge_energy_sp', float), ('discharge_energy_sp', float),
                    ('energy_efficiency', lambda x: float(x[:-1]))]
                    
     
    def __init__(self, cycle_header):
        """ Initialize a Cycle object.

        Parameters
        ----------
        cycle_header : str
            Header containing infos about the cycle
        """

        self.properties = collections.OrderedDict()
        self.steps = collections.OrderedDict()
        
        #--- Parse header and populate properties dictionary
        self._parse_header(cycle_header)

    def __str__(self):
        #--- Returns pretty representation of a Cycle object
        #    if printed with str.print()
        return "Cycle_id: " + self.cycle_id

    def _parse_header(self, header_line):
        #--- Split header line
        header = header_line.split('\t')

        #--- Populate the properties dictionary with values from header
        for idx, entry in enumerate(Cycle.head_entries):
            # entry[1] is a function that converts the string to the right type
            self.properties[entry[0]] = entry[1](header[idx])

    def _add_step(self, step_header):
        #--- Adds a step to the cycle object

        #--- Create a step object
        step = Step(step_header, self.properties['cycle_id'])

        #--- Add it to the steps dictionary in the cycle object
        self.steps[step.label] = step

        #--- Return the step label (so that the parser know where to add data)
        return step.label

    def get_duration(self):
        """ Returns total duration of a battery (rest)-charge-discharge cycle.

        Returns
        -------
        dt.timedelta
            timedelta object containing total duration of the battery cycle.
        """

        return np.sum([step.duration for step in self.steps.values()])

    def get_efficiency(self, mode = 'standard'):
        """ Returns efficiency of the cycle.

        Parameters
        ----------
        mode : str {'standard', 'inverse'}
            if 'standard', return discharge/charge time, otherwise its inverse.

        Returns
        -------
        float
            efficiency of the cycle
        """
        
        discharge_time = self.steps['CC_DChg'].duration
        charge_time = self.steps['CC_Chg'].duration

        if mode == 'standard':
            return discharge_time/charge_time
        elif mode == 'inverse':
            return charge_time/discharge_time
        else:
            raise ValueError(
                "'mode' argument accepts only 'standard' or 'inverse' parameters.") 
       
    def plot_voltage(self, step='all'):
        """ Plot voltage of a cycle as a function of the record index.

        Parameters
        ----------
        step : str {'all', 'charge', 'discharge'}
            Defines which step of a cycle should be plotted.
        """

        #--- Take all values in cycle step dictionary is step is 'all'
        if step == 'all':
            idx = []
            voltages = []

            for step in self.steps.values():
                idx.extend(step.records['id'])
                voltages.extend(step.records['volt'])
        elif step == 'charge':
            idx = self.steps['CC_Chg'].records['id']
            voltages = self.steps['CC_Chg'].records['volt']
        elif step == 'discharge':
            idx = self.steps['CC_DChg'].records['id']
            voltages = self.steps['CC_DChg'].records['volt']
        else:
            raise ValueError(
                "'step' argument can take 'all', 'charge', discharge' parameters only.")

        #--- Plot with matplotlib
        plt.plot(idx, voltages)
        plt.show()


class Step(object):
    """ Contains informations about either a rest, charge or discharge step.
    """

    def __init__(self, step_header, parent_cycle_id):
        """ Initialize a step object.

        Parameters
        ----------
        step_header : str
            Contains the header preceeding all records in a step
        parent_cycle_id : str
            Id of the cycle whose the step belongs.
        """

        #--- Attributes are quite self explanatory
        header = step_header.split('\t')
        self.parent_cycle_id = int(parent_cycle_id)
        self.step_id = int(header[1])
        self.label = header[2]
        self.capacity = float(header[4])
        self.specific_capacity = float(header[5])
        self.energy = float(header[6])
        self.specific_energy = float(header[7])
        self.capacitance = float(header[8])
        self.voltage_start = float(header[9])
        self.voltage_end = float(header[10])

        #--- Variables defined outside __init__
        self.id_range = None

        #--- Contains data for each record
        self.records = {}

        #--- Compute volt(end) - volt(start)
        self.voltage_delta = self.voltage_end - self.voltage_start

        #--- Duration of the step
        hours, minutes, seconds, milliseconds = header[3].split(':')
        self.duration = dt.timedelta(hours=int(hours), minutes=int(minutes),
                                     seconds=int(seconds))

    def __str__(self):
        #--- Returns pretty representation of a Step object
        #    if printed with str.print()
        return ("Step " + str(self.step_id) + " type "
                + self.label + " of Cycle " + str(self.parent_cycle_id))

    def _add_records(self, record_list):
        #--- Adds records to a step object

        # str: contains all record lines of a step in one single string
        # replace the space between date and time in the last column with a T
        # so that the datetime format is iso compliant
        string = ''.join(record_list).replace(' ', 'T')

        # --- Create a StringIO object that can be parsed by numpy.loadtxt()
        csv = StringIO(string)

        # func : lambda function to conver bytestring to string on the fly
        bstr2str = lambda x: str(x, encoding='utf-8')

        # For the sake of brevity (sigh...)
        records = self.records

        # Read records into keys of the step records dictionary
        records['id'], \
            records['rel_time'], \
            records['volt'], \
            records['capacity'], \
            records['sp_capacity'], \
            records['time'] = np.loadtxt(csv,
                                         usecols=(0, 1, 2, 5, 6, 9),
                                         unpack=True,
                                         dtype=[('id', np.int),
                                                ('rel_time', 'timedelta64[s]'),
                                                ('volt', np.float64),
                                                ('capacity', np.float64),
                                                ('sp_capacity', np.float64),
                                                ('time', 'datetime64[ms]')],
                                         converters={1: bstr2timedelta,
                                                     9: bstr2str})

        #--- Save the minimum and maximum record id of the step
        self.id_range = (self.records['id'][1], self.records['id'][-1])
