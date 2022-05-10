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
          
    def set_name(self,string):
        """ Set name of system imager (60 caracters)
            Example :SA200-UT1, SA200-178MM-F200, ...
        """
        self.set_block(5,string)
        return string

    def get_name(self):
        """ Set name of system imager (60 caracters)
            Example :SA200-UT1, SA200-178MM-F200, ...
        """
        s = self.get_block(5)
        return s 

    def set_coverage(self,min=3000,max=7000):
        """ Set system spectrum coverage 
            Used block06 (min) and block07 (max)
        """
        self.set_block(6,str(min))
        self.set_block(7,str(max))
        return min,max

    def get_coverage(self,pixel_size=2.4):
        """ Get system spectrum coverage 
            Used block06 min and block07 max
        """
        d = self.dispersion(pixel_size)
        min = int(float(self.get_block(6)) / d)
        max = int(float(self.get_block(7)) / d) 
        return min,max

    def dispersion(self,pixel_size):
        """ Get system dispersion (nanomètre)
            pixel_size : um
        """
        l = self.get_length()
        R = self.get_R()
        d=(10000*pixel_size/(float(l)*float(R))/10)
        return d
            
    def shemas(self):
        from IPython.display import Image
        display(Image('ciboulette/indiclient/draw/shemas.png'))
        
