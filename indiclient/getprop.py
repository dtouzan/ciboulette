# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with indiserver via the INDI protocol, http://www.indilib.org.
"""

__authors__ = ("Dominique Touzan","ciboulette module")
__contact__ = ("dtouzan@gmail.com","https://github.com/dtouzan/ciboulette")
__copyright__ = "MIT"
__date__ = "2024-11-02"
__version__= "1.0.0"

import time
import io

import logging
import logging.handlers

from .indiclient import indiclient
from .getproplist import list_pylibcamera

log = logging.getLogger("")
log.setLevel(logging.INFO)


class indi_getprop(indiclient):
        
    def __init__(self, host, port):
        super(indi_getprop, self).__init__(host, port)
        self.list_getprop = list_pylibcamera

    @property
    def getprop(self):
        for line in self.list_getprop:
            value = line.split('.')
            driver = value[0]
            vector = value[1]
            element = value[2]
            values = self.get_text(driver, vector, element)
            print(f'{line}={values}')
    
    def properties(self, string=list()):
        for line in string:
            value = line.split('.')
            driver = value[0]
            vector = value[1]
            element = value[2]
            values = self.get_text(driver, vector, element)
            print(f'{line}={values}')

    def connect(self, driver='indi_pylibcamera'):
        """
        Enable camera connection
        """
        self.set_and_send_switchvector_by_elementlabel(driver, "CONNECTION", "Connect")

    def disconnect(self, driver='indi_pylibcamera'):
        """
        Disable camera connection
        """
        self.set_and_send_switchvector_by_elementlabel(driver, "CONNECTION", "Disconnect")











