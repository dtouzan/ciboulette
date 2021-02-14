# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with cameras via the INDI protocol, http://www.indilib.org.
"""

import time
import io

import logging
import logging.handlers

from astropy.io import fits

from .indiclient import indiclient
from ciboulette.indiclient.indicam import CCDCam

log = logging.getLogger("")
log.setLevel(logging.INFO)

class ASICam120Mini(CCDCam):
    """
    Wrap CCDCam, set driver to ASI CCD, and point to localhost by default.
    """
    def __init__(self, host='localhost', port=7624):
        super(ASICam120Mini, self).__init__(host, port, driver="ZWO CCD ASI120MM Mini")
        self.camera_name = "ZWO ASI Camera"
        self.process_events()

    @property
    def filters(self):
        return ["N/A"]

    @property
    def filter(self):
        return "N/A"

    @filter.setter
    def filter(self, f):
        pass

    @property
    def gain(self):
        self.process_events()
        gain = self.get_float(self.driver, "CCD_CONTROLS", "Gain")
        return gain

