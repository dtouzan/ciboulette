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
from ciboulette.indiclient.indimount import Telescope

log = logging.getLogger("")
log.setLevel(logging.INFO)

class EQMod(Telescope):
    """
    Wrap Mount, set driver to EQMod mount, and point to localhost by default.
    """
    def __init__(self, host='localhost', port=7624):
        super(EQMod, self).__init__(host, port, driver="EQMod Mount")
        self.mount_name = "EQMod"
        self.process_events()
        
