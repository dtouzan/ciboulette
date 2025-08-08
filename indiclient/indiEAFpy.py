# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with cameras via the INDI protocol, http://www.indilib.org.

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
__date__ = "2025-08-03"
__version__= "1.0.0"
__citation__ = "MMT Observatory package. https://github.com/MMTObservatory/indiclient"

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
        super(EAFpy, self).__init__(host, port, driver="EAFpy_Focuser")
        self.focuser_name = "EAFpy"

    @property
    def default(self):
        """
        Configure Focuser to speed 1, timer 10ms, Increment 25, direction
        """
    
    @property
    def ticks(self):
        """
        Return ticks and init 0
        """
        value = self.get_text(self.driver, "REL_FOCUS_POSITION", "FOCUS_RELATIVE_POSITION")
        return int(value)

    @ticks.setter
    def ticks(self,value=25):
        """
        Set Ticks with value 0<ticks<500
        """
        if  0<= value <=500:
            self.set_and_send_float(self.driver, 'REL_FOCUS_POSITION', 'FOCUS_RELATIVE_POSITION', value) 
            self.process_events()

    @property
    def speed(self):
        """
        Return speed
        """
        Speed_1 = self.get_text(self.driver, "FOCUS_SPEED_SP", "FOCUS_SPEED_1")
        Speed_2 = self.get_text(self.driver, "FOCUS_SPEED_SP", "FOCUS_SPEED_2")
        return Speed_1, Speed_2

    @property
    def speed1(self):
        """
        Set Speed
        """
        self.set_and_send_text(self.driver, 'FOCUS_SPEED_SP', 'FOCUS_SPEED_2', 'Off')
        self.set_and_send_text(self.driver, 'FOCUS_SPEED_SP', 'FOCUS_SPEED_1', 'On')
    
    @property
    def speed2(self):
        """
        Set Speed
        """
        self.set_and_send_text(self.driver, 'FOCUS_SPEED_SP', 'FOCUS_SPEED_1', 'Off')
        self.set_and_send_text(self.driver, 'FOCUS_SPEED_SP', 'FOCUS_SPEED_2', 'On')

        
    @property
    def delay(self):
        """
        Return delay 
        """
        self.process_events()
        value = self.get_float(self.driver, "DELAY", "DELAY_VALUE")
        return value

    @delay.setter
    def delay(self,value=10):
        """
        Set delay
        """
        if  2<= value <=25:
            self.set_and_send_float(self.driver, 'DELAY', 'DELAY_VALUE', value) 
            self.process_events()
            
    @property
    def direction(self):
        """
        Return direction 
        """
        Focus_In = self.get_text(self.driver, "FOCUS_MOTION", "FOCUS_INWARD")
        Focus_Out = self.get_text(self.driver, "FOCUS_MOTION", "FOCUS_OUTWARD")
        return Focus_In, Focus_Out

    @property
    def inward(self):
        """
        Set inward
        """
        self.set_and_send_text(self.driver, 'FOCUS_MOTION', 'FOCUS_OUTWARD', 'Off')
        self.set_and_send_text(self.driver, 'FOCUS_MOTION', 'FOCUS_INWARD', 'On')

    @property
    def outward(self):
        """
        Set outward
        """
        self.set_and_send_text(self.driver, 'FOCUS_MOTION', 'FOCUS_INWARD', 'Off')
        self.set_and_send_text(self.driver, 'FOCUS_MOTION', 'FOCUS_OUTWARD', 'On')

