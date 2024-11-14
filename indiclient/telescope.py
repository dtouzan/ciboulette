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
from astropy.table import Table
from astropy.time import Time

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
        """
        Set BAUD_RATE at 115200 : https://www.indilib.org/devices/telescopes/eqmod.html
        
        For ubuntu server 20.10 , configure the /dev/ttyUSB0 for set 115200 baud rate
        https://stackoverflow.com/questions/42290052/how-to-set-baud-rate-automatically-when-device-connects
        
        Create file rules /etc/udev/rules.d/99-eqmod.rules and reboot
        
        #99-eqmod.rules
        ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", RUN+="/bin/stty -F /dev/%k 115200"
        
        For idVendor and idProduct use lsusb for example on RASPBERRY PI4 ubuntu server 20.10
        ubuntu@ubuntu:/etc/udev/rules.d$ lsusb
        Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
        Bus 001 Device 004: ID 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC
        Bus 001 Device 003: ID 03c3:120c  USB2.0 Hub
        Bus 001 Device 002: ID 2109:3431 VIA Labs, Inc. Hub
        Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
        
        https://github.com/indilib/indi-3rdparty/tree/master/indi-eqmod:
        ================================================================
        The mount is supposed to be parked in the home position (pointing to the celestial pole) 
        at the first connection, or after each reset of the mount.
        """
        self.baud_rate = '9600'
        
    @property    
    def baud_rate(self):
        """
        Return BAUD_RATE mode, return astropy table
        9600, 19200, 38400, 57600, 115200, 230400
        """        
        p = Table()
        p['9600'] = [self.get_text(self.driver, "DEVICE_BAUD_RATE", "9600")]
        p['19200'] = [self.get_text(self.driver, "DEVICE_BAUD_RATE", "19200")]
        p['38400'] = [self.get_text(self.driver, "DEVICE_BAUD_RATE", "38400")]
        p['57600'] = [self.get_text(self.driver, "DEVICE_BAUD_RATE", "57600")]
        p['115200'] = [self.get_text(self.driver, "DEVICE_BAUD_RATE", "115200")]
        p['230400'] = [self.get_text(self.driver, "DEVICE_BAUD_RATE", "230400")]
        return p

    @baud_rate.setter
    def baud_rate(self,label):
        """
        Set BAUD_RATE 
        """
        if label in ('9600','19200','38400','57600','115200','23040'):
            vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "DEVICE_BAUD_RATE", label)       
            if self.debug:
                vec.tell()               

    @property
    def telescope_slew_rate(self):    
        """
        Return TELESCOPE_SLEW_RATE mode, return astropy table
        """
        p = Table()
        p['1x'] = [self.get_text(self.driver, "TELESCOPE_SLEW_RATE", "1x")]
        p['2x'] = [self.get_text(self.driver, "TELESCOPE_SLEW_RATE", "2x")]
        p['3x'] = [self.get_text(self.driver, "TELESCOPE_SLEW_RATE", "3x")]
        p['4x'] = [self.get_text(self.driver, "TELESCOPE_SLEW_RATE", "4x")]
        p['5x'] = [self.get_text(self.driver, "TELESCOPE_SLEW_RATE", "5x")]
        p['6x'] = [self.get_text(self.driver, "TELESCOPE_SLEW_RATE", "6x")]
        p['7x'] = [self.get_text(self.driver, "TELESCOPE_SLEW_RATE", "7x")]
        p['8x'] = [self.get_text(self.driver, "TELESCOPE_SLEW_RATE", "8x")]
        p['9x'] = [self.get_text(self.driver, "TELESCOPE_SLEW_RATE", "9x")]
        return p

    @telescope_slew_rate.setter
    def telescope_slew_rate(self,f):
        """
        Set TELESCOPE_SLEW_RATE. 1 to 9
        """
        if f >= 1 and f <=9:                
            labels = ['1x','2x','4x','8x','32x','64x','128x','600x','700x']
            label = labels[f - 1]  
            vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "TELESCOPE_SLEW_RATE", label)       
            if self.debug:
                vec.tell()               

    @property
    def auxencoder(self,label = 'N'):
        return None

    @auxencoder.setter
    def auxencoder(self,label = 'N'):
        """
        Set AUXENCODER Yes or No
        """
        if label == 'Y':
            vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "AUXENCODER", "On")       
            if self.debug:
                vec.tell()      
        if label == 'N':
            vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "AUXENCODER", "Off")       
            if self.debug:
                vec.tell()                         

    @property
    def ppec(self):
        value = self.get_text(self.driver, "PPEC", "PPEC_ON")
        if value == "On":
            return True
        else:
            return False

    @ppec.setter
    def ppec(self, label = 'Y'):
        """
        Set PPEC Yes, PPEC.PPEC_ON=On
        """
        if label == 'Y':
            self.set_and_send_text(self.driver, "PPEC", "PPEC_OFF", "Off") 
            vec = self.set_and_send_text(self.driver, "PPEC", "PPEC_ON", "On")   
            if self.debug:
                vec.tell() 
        if label == 'N':
            self.set_and_send_text(self.driver, "PPEC", "PPEC_ON", "Off") 
            vec = self.set_and_send_text(self.driver, "PPEC", "PPEC_OFF", "On") 
            if self.debug:
                vec.tell() 

    @property
    def RA(self):
        """
        Return the telescope's right ascension coordinate.
         The right ascension (hours) of the telescope's current equatorial
         coordinates, in the coordinate system given by the EquatorialSystem
         property.
        """
        return self.rightascension

    @property
    def DEC(self):
        """
        Return the telescope's declination.
         Reading the property will raise an error if the value is unavailable.
         The declination (degrees) of the telescope's current equatorial coordinates,
         in the coordinate system given by the EquatorialSystem property.        
        """
        return self.declination

    @property
    def observatory(self):
        """
        Return site Longitude, latitude and elevation
        """
        observatory_info = {
            'longitude': self.sitelongitude,
            'latitude': self.sitelatitude,
            'elevation': self.siteelevation
        }
        return observatory_info

    @property
    def coords(self):
        """
        Return site RA an Dec
        """
        coords_info = {
            'RA': self.RA,
            'DEC': self.DEC,
        }
        return coords_info

    @property
    def baud_rate_115200(self):
        """
        Set baud rate 115200
        """
        self.baud_rate = '115200'

class EQsimul(Telescope):

    def __init__(self, host='localhost', port=7624):
        super(EQsimul, self).__init__(host, port, driver="Telescope Simulator")
        self.mount_name = "EQsimul"

    @property
    def RA(self):
        """
        Return the telescope's right ascension coordinate.
         The right ascension (hours) of the telescope's current equatorial
         coordinates, in the coordinate system given by the EquatorialSystem
         property.
        """
        return self.rightascension

    @property
    def DEC(self):
        """
        Return the telescope's declination.
         Reading the property will raise an error if the value is unavailable.
         The declination (degrees) of the telescope's current equatorial coordinates,
         in the coordinate system given by the EquatorialSystem property.        
        """
        return self.declination

    @property
    def observatory(self):
        """
        Return site Longitude, latitude and elevation
        """
        observatory_info = {
            'longitude': self.sitelongitude,
            'latitude': self.sitelatitude,
            'elevation': self.siteelevation
        }
        return observatory_info

    @property
    def coords(self):
        """
        Return site RA an Dec
        """
        coords_info = {
            'RA': self.RA,
            'DEC': self.DEC,
        }
        return coords_info






















