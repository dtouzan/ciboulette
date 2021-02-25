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
        self.raw16

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

    @gain.setter
    def gain(self,f):
        if f >=0 and f <=100:
            self.set_and_send_float(self.driver, 'CCD_CONTROLS', 'Gain', f) 
            self.process_events()

    @property
    def raw16(self):
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "CCD_VIDEO_FORMAT", "Raw 16 bit")
        if self.debug:
            vec.tell()
        return vec

class ATIKCam383L(CCDCam):
    """
    Wrap CCDCam, set driver to ATIK 383L+ CCD, and point to localhost by default.
    """
    def __init__(self, host='localhost', port=7624):
        super(ATIKCam383L, self).__init__(host, port, driver="Atik 383L")
        self.camera_name = "Atik"
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

    def local(self):
        """
        Enable local write
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "UPLOAD_MODE", "Local")
        if self.debug:
            vec.tell()
        return vec

    def client(self):
        """
        Enable client write
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "UPLOAD_MODE", "Client")
        if self.debug:
            vec.tell()
        return vec

    def both(self):
        """
        Enable both write
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "UPLOAD_MODE", "Both")
        if self.debug:
            vec.tell()
        return vec

 
    @property
    def updir(self):
        upload_dir = self.get_text(self.driver, "UPLOAD_SETTINGS", "UPLOAD_DIR")
        return upload_dir

    @updir.setter
    def updir(self,string):
        """
        Configure UPLOAD_DIR : IMAGE_XXX
        """
        self.set_and_send_text(self.driver, "UPLOAD_SETTINGS", "UPLOAD_DIR", string)

    @property
    def prefix(self):
        upload_prefix = self.get_text(self.driver, "UPLOAD_SETTINGS", "UPLOAD_PREFIX")
        return upload_prefix      
        
    @prefix.setter
    def prefix(self,string):
        """
        Configure UPLOAD_PREFIX : IMAGE_XXX
        """
        self.set_and_send_text(self.driver, "UPLOAD_SETTINGS", "UPLOAD_PREFIX", string)
