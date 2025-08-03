# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with cameras via the INDI protocol, http://www.indilib.org.

# indi_EAFpy_focuser

"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2025-07-28"
__version__= "1.0.0"

import time
import io

import logging
import logging.handlers

from astropy.io import fits

from .indiclient import indiclient
from ciboulette.indiclient.indifocuser import Focuser

log = logging.getLogger("")
log.setLevel(logging.INFO)

class EAFpy(Focuser):
    """
    Wrap EAFpy,set the driver to the EAFpy driver 
    """
    def __init__(self, host="localhost", port=7624):
        super(EAFpy, self).__init__(host, port, driver="indi_EAFpy_focuser")
        self.focuser_name = "EAFpy"

    @property
    def default(self):
        """
        Configure Focuser to speed 1, timer 10ms, Increment 25, direction
        """
    
    @property
    def ticks(self):
        """
        Retur indi_EAFpy_focuser_FOCUSER.TICKS
        """

    @ticks.setter
    def ticks(self,value=25):
        """
        Set Ticks and go
        """

    @property
    def speed(self):
        """
        Return speed
        """

    @speed.setter
    def speed(self,value=1):
        """
        Set Speed
        """
        
    @property
    def timer(self):
        """
        Return timer 
        """

    @timer.setter
    def timer(self,value=10):
        """
        Set timer
        """
    @property
    def direction(self):
        """
        Return direction 
        """

    @direction.setter
    def direction(self,value=In):
        """
        Set direction
        """
    
