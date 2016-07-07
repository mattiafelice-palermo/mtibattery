"""Helper functions
"""

import numpy as np
import datetime as dt

def bstr2timedelta(data):
    """ Converts a byte string to a timedelta object

    Parameters
    ----------
    data : bytestring
        Contains a bytestring representing a timedelta

    Returns
    -------
    dt.timedelta
        timedelta object
    """
    string = str(data)
    # Use string starting from character 2 in order to remove
    # the "b'" preceding the string in a byte string
    hours, minutes, seconds, milliseconds = string[2:].split(':')
    time = dt.timedelta(hours=int(hours), minutes=int(
        minutes), seconds=int(seconds)).total_seconds()
    return np.timedelta64(int(time), 's')


def str2timedelta(data):
    """ Converts a string to a timedelta object

    Parameters
    ----------
    data : string
        Contains a string representing a timedelta

    Returns
    -------
    dt.timedelta
        timedelta object
    """
    string = str(data)
    # Use string starting from character 2 in order to remove
    # the "b'" preceding the string in a byte string
    hours, minutes, seconds = string.split(':')
    time = dt.timedelta(hours=int(hours), minutes=int(
        minutes), seconds=int(seconds)).total_seconds()
    return time

