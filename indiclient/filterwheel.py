# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with filterwheel a the INDI protocol, http://www.indilib.org.
"""

import time
import io

import logging
import logging.handlers

from astropy.io import fits

from .indiclient import indiclient
from ciboulette.indiclient.indifilter import FILTERWheel

log = logging.getLogger("")
log.setLevel(logging.INFO)

class FILTERWheelSimulator(FILTERWheel):
    """
    Wrap FILTERWheel, set driver to FILTERWHEEL Simulator, and point to localhost by default.
    """
    def __init__(self, host='localhost', port=7624):
        super(FILTERWheelSimulator, self).__init__(host, port, driver="Filter Simulator")
        self.filter_name = "Filter Simulator"
        self.process_events()


class FILTERWheelATIK(FILTERWheel):
    """
    Wrap FILTERWheel, set driver to FILTERWHEEL ATIK, and point to localhost by default.
    """
    def __init__(self, host='localhost', port=7624):
        super(FILTERWheelATIK, self).__init__(host, port, driver="Atik EFW2")
        self.filter_name = "Atik"
        self.process_events()

