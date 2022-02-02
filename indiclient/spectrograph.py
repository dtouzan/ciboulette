# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with spectrograph a the INDI protocol, http://www.indilib.org.
"""

import time
import io

import logging
import logging.handlers

from .indiclient import indiclient
from ciboulette.indiclient.indisa200 import SA200Motor

log = logging.getLogger("")
log.setLevel(logging.INFO)

class SPECTROGRAPHsa200(SA200Motor):
    """
    Wrap SA200, set driver to SA200 motor, and point to localhost by default.
    """
    def __init__(self, host='localhost', port=7624):
        super(SPECTROGRAPHsa200, self).__init__(host, port, driver="SA200")
        self.filter_name = "SA200"
        self.process_events()