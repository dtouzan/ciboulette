# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with mount a the INDI protocol, http://www.indilib.org.

# indi_EAFpy_focuser
EAFpy_Focuser.CONNECTION.CONNECT=On
EAFpy_Focuser.CONNECTION.DISCONNECT=Off
EAFpy_Focuser.DRIVER_INFO.DRIVER_NAME=EAFpy_Focuser
EAFpy_Focuser.DRIVER_INFO.DRIVER_EXEC=indi_EAFpy_focuser
EAFpy_Focuser.DRIVER_INFO.DRIVER_VERSION=1.2
EAFpy_Focuser.DRIVER_INFO.DRIVER_INTERFACE=8
EAFpy_Focuser.DEBUG.ENABLE=Off
EAFpy_Focuser.DEBUG.DISABLE=On
EAFpy_Focuser.POLLING_PERIOD.PERIOD_MS=1000
EAFpy_Focuser.SIMULATION.ENABLE=Off
EAFpy_Focuser.SIMULATION.DISABLE=On
EAFpy_Focuser.CONFIG_PROCESS.CONFIG_LOAD=Off
EAFpy_Focuser.CONFIG_PROCESS.CONFIG_SAVE=Off
EAFpy_Focuser.CONFIG_PROCESS.CONFIG_DEFAULT=Off
EAFpy_Focuser.CONFIG_PROCESS.CONFIG_PURGE=Off
EAFpy_Focuser.FOCUS_MOTION.FOCUS_INWARD=On
EAFpy_Focuser.FOCUS_MOTION.FOCUS_OUTWARD=Off
EAFpy_Focuser.REL_FOCUS_POSITION.FOCUS_RELATIVE_POSITION=50
EAFpy_Focuser.FOCUS_ABORT_MOTION.ABORT=Off
EAFpy_Focuser.USEJOYSTICK.ENABLE=Off
EAFpy_Focuser.USEJOYSTICK.DISABLE=On
EAFpy_Focuser.SNOOP_JOYSTICK.SNOOP_JOYSTICK_DEVICE=Joystick
EAFpy_Focuser.FOCUS_SPEED_SP.FOCUS_SPEED_1=On
EAFpy_Focuser.FOCUS_SPEED_SP.FOCUS_SPEED_2=Off
EAFpy_Focuser.DELAY.DELAY_VALUE=10
EAFpy_Focuser.USEJOYSTICK.ENABLE=Off
EAFpy_Focuser.USEJOYSTICK.DISABLE=On
EAFpy_Focuser.SNOOP_JOYSTICK.SNOOP_JOYSTICK_DEVICE=Joystick
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
from astropy.table import Table

from .indiclient import indiclient

log = logging.getLogger("")
log.setLevel(logging.INFO)

class Focuser(indiclient):
    """
    Wrap indiclient.indiclient with some filter-specific utility functions to simplify things like taking,
    mount, etc.
    """
    def __init__(self, host, port, driver="Focuser simulator", debug=True):
        super(Focuser, self).__init__(host, port)
        self.focuser_name = "Focuser Default"
        self.driver = driver
        self.debug = debug
        if not self.connected:
            self.connect()
            time.sleep(2)

        # run this to clear any queued events
        self.process_events()
        self.defvectorlist = []
        self.vector_dict = {v.name: v for v in self.indivectors.list}

    @property
    def connected(self):
        """
        Check connection status and return True if connected, False otherwise.
        """
        status = self.get_text(self.driver, "CONNECTION", "CONNECT")
        if status == 'On':
            return True
        else:
            return False

    def connect(self):
        """
        Enable focuser connection
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "CONNECTION", "Connect")
        if self.debug and vec is not None:
            vec.tell()
        self.process_events()
        return vec

    def disconnect(self):
        """
        Disable mount connection
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "CONNECTION", "Disconnect")
        if self.debug:
            vec.tell()
        return vec

    def _default_def_handler(self, vector, indi):
        """
        Overload the default vector handler to do a vector.tell() so it's clear what's going on
        """
        if self.debug:
            vector.tell()
        pass
            
    @property 
    def abort(self):
        """
        Set TELESCOPE_ABORT_MOTION
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "TELESCOPE_ABORT_MOTION", 'Abort')       
        if self.debug:
            vec.tell()

    @property 
    def load(self):      
        """Load indilid configuration file .xml
        """
        self.set_and_send_text(self.driver, "CONFIG_PROCESS", "CONFIG_LOAD", "On")
        return True

    @property 
    def save(self):      
        """Save indilid configuration file .xml
        """
        self.set_and_send_text(self.driver, "CONFIG_PROCESS", "CONFIG_SAVE", "On")
        return True 
