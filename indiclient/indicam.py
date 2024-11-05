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
from astropy.table import Table

log = logging.getLogger("")
log.setLevel(logging.INFO)


class CCDCam(indiclient):
    """
    Wrap indiclient.indiclient with some camera-specific utility functions to simplify things like taking,
    exposures, configuring camera binning, etc.
    """
    def __init__(self, host, port, driver="CCD Simulator", debug=True):
        super(CCDCam, self).__init__(host, port)
        self.camera_name = "UT1 Default"
        self.enable_blob()
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
    def ccd_info(self):
        """
        Get the CCD info about pixel sizes and bits per pixel, etc.
        """
        info_vec = self.get_vector(self.driver, "CCD_INFO")
        info = {}
        for e in info_vec.elements:
            info[e.getName()] = e.get_float()
        return info

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

    @property
    def observer(self):
        obs = self.get_text(self.driver, "FITS_HEADER", "FITS_OBSERVER")
        return obs

    @observer.setter
    def observer(self, string):
        self.set_and_send_text(self.driver, "FITS_HEADER", "FITS_OBSERVER", string)

    @property
    def object(self):
        obj = self.get_text(self.driver, "FITS_HEADER", "FITS_OBJECT")
        return obj

    @object.setter
    def object(self, string):
        self.set_and_send_text(self.driver, "FITS_HEADER", "FITS_OBJECT", string)

    @property
    def temperature(self):
        self.process_events()
        t = self.get_float(self.driver, "CCD_TEMPERATURE", "CCD_TEMPERATURE_VALUE")
        return t

    @temperature.setter
    def temperature(self, temp):
        curr_t = self.get_float(self.driver, "CCD_TEMPERATURE", "CCD_TEMPERATURE_VALUE")
        if temp != curr_t:
            self.set_and_send_float(self.driver, "CCD_TEMPERATURE", "CCD_TEMPERATURE_VALUE", temp)
        self.process_events()

    @property
    def cooling_power(self):
        self.process_events()
        power = self.get_float(self.driver, "CCD_COOLER_POWER", "CCD_COOLER_VALUE")
        return power

    @property
    def cooler(self):
        cooler = self.get_text(self.driver, "CCD_COOLER", "COOLER_ON")
        return cooler

    @property
    def fan(self):
        fan = self.get_text(self.driver, "CCD_FAN", "FAN_ON")
        return fan

    @property
    def frame_types(self):
        """
        Return: ['Light', 'Bias', 'Dark', 'Flat']
        """
        types = [e.label for e in self.get_vector(self.driver, "CCD_FRAME_TYPE").elements]
        return types

    @property
    def filters(self):
        """
        Return list of names of installed filters
        """
        filters = [e.get_text() for e in self.get_vector(self.driver, "FILTER_NAME").elements]
        return filters

    @property
    def filter(self):
        """
        Return: name selected filter
        """
        slot = int(self.get_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE")) - 1  # filter slots 1-indexed
        if slot >= 0 and slot < len(self.filters):
            f = self.filters[slot]
        else:
            f = None
        return f

    @filter.setter
    def filter(self, f):
        """
        Select filter index
        Set: Filter number  
        """
        if isinstance(f, int):
            if f >= 0 and f < len(self.filters):
                self.set_and_send_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE", f)
        else:
            if f in self.filters:
                self.set_and_send_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE", self.filters.index(f)+1)

    @property
    def binning(self):
        """
        Get the X and Y binning that is currently set. Different cameras have different restrictions on how binning
        can be set so configure the @setter on a per class basis.
        """
        bin_vec = self.get_vector(self.driver, "CCD_BINNING")
        binning = {}
        for e in bin_vec.elements:
            binning[e.label] = e.get_int()
        return binning

    @binning.setter
    def binning(self, bindict):
        """
        Set binning from a dict of form of e.g. {'X':2, 'Y':2}
        """
        if 'X' in bindict:
            if bindict['X'] >= 1:
                self.set_and_send_float(self.driver, "CCD_BINNING", "HOR_BIN", int(bindict['X']))
                log.info("Setting X binning to %d" % int(bindict['X']))

        if 'Y' in bindict:
            if bindict['Y'] >= 1:
                self.set_and_send_float(self.driver, "CCD_BINNING", "VER_BIN", int(bindict['Y']))
                log.info("Setting Y binning to %d" % int(bindict['Y']))

    @property
    def frame(self):
        """
        Get the frame configuration of the CCD: X lower, Y lower, width, and height
        """
        xl = self.get_float(self.driver, "CCD_FRAME", "X")
        yl = self.get_float(self.driver, "CCD_FRAME", "Y")
        xu = self.get_float(self.driver, "CCD_FRAME", "WIDTH")
        yu = self.get_float(self.driver, "CCD_FRAME", "HEIGHT")
        frame_info = {
            'X': xl,
            'Y': yl,
            'width': xu,
            'height': yu
        }
        return frame_info

    @frame.setter
    def frame(self, framedict):
        """
        Configure area of CCD to readout where framedict is of the form:
        {
            "X": int - lower X value of readout region
            "Y": int - lower Y value of readout region
            "width": int - width of the readout region
            "height": int - height of the readout region
        }
        """
        ccdinfo = self.ccd_info
        if 'X' in framedict:
            if framedict['X'] >= 0 and framedict['X'] <= ccdinfo['CCD_MAX_X']:
                self.set_and_send_float(self.driver, "CCD_FRAME", "X", int(framedict['X']))
                log.info("Setting lower X to %d" % int(framedict['X']))
                if 'width' in framedict:
                    newwidth = min(framedict['width'], ccdinfo['CCD_MAX_X']-framedict['X'])
                    if newwidth >= 1:
                        self.set_and_send_float(self.driver, "CCD_FRAME", "WIDTH", int(newwidth))
                        log.info("Setting width to %d" % int(newwidth))
        if 'Y' in framedict:
            if framedict['Y'] >= 0 and framedict['Y'] <= ccdinfo['CCD_MAX_Y']:
                self.set_and_send_float(self.driver, "CCD_FRAME", "Y", int(framedict['Y']))
                log.info("Setting lower Y to %d" % int(framedict['Y']))
                if 'height' in framedict:
                    newheight = min(framedict['height'], ccdinfo['CCD_MAX_Y']-framedict['Y'])
                    if newheight >= 1:
                        self.set_and_send_float(self.driver, "CCD_FRAME", "HEIGHT", int(newheight))
                        log.info("Setting height to %d" % int(newheight))

    def connect(self):
        """
        Enable camera connection
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "CONNECTION", "Connect")
        if self.debug and vec is not None:
            vec.tell()
        self.process_events()
        return vec

    def disconnect(self):
        """
        Disable camera connection
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

    def cooling_on(self):
        """
        Turn the cooler on
        """
        c_vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "CCD_COOLER", "On")
        self.process_events()
        return c_vec

    def cooling_off(self):
        """
        Turn the cooler off
        """
        c_vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "CCD_COOLER", "Off")
        self.process_events()
        return c_vec


    @property
    def abort(self):
        """
        Abort the current exposure, if any, and returns the camera to Idle state.
        """ 
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "CCD_ABORT_EXPOSURE", "On")
        self.ctrl = 0
        self.process_events()
        return vec

    @property
    def ready(self):
        """
        IMX 477 control camera
        Return  CAMCTRL_EXPOSUREVALUE.EXPOSUREVALUE, 0 ready, 1 in shoot, ...
        """ 
        value = self.get_float(self.driver, "CAMCTRL_EXPOSUREVALUE", "EXPOSUREVALUE")
        if value==0:
            return True
        else:
            return False

    @property
    def ctrl(self):
        """
        IMX 477 control camera
        Return  CAMCTRL_EXPOSUREVALUE.EXPOSUREVALUE, 0 ready, 1 in shoot, ...
        """ 
        value = self.get_float(self.driver, "CAMCTRL_EXPOSUREVALUE", "EXPOSUREVALUE")
        return value
        
    @ctrl.setter
    def ctrl(self, ctrl_value=0):
        """
        IMX 477 control camera
        set  CAMCTRL_EXPOSUREVALUE.EXPOSUREVALUE, 0 ready, 1 shoot, ...
        """ 
        self.set_and_send_float(self.driver, "CAMCTRL_EXPOSUREVALUE", "EXPOSUREVALUE", ctrl_value)       
     
    @property
    def activedevices(self):
        """
        Return ACTIVE_DEVICES mode, return astropy table
        """
        p = Table()
        p['TELESCOPE'] = [self.get_text(self.driver, "ACTIVE_DEVICES", "ACTIVE_TELESCOPE")]
        p['ROTATOR'] = [self.get_text(self.driver, "ACTIVE_DEVICES", "ACTIVE_ROTATOR")]
        p['FOCUSER'] = [self.get_text(self.driver, "ACTIVE_DEVICES", "ACTIVE_FOCUSER")]
        p['FILTER'] = [self.get_text(self.driver, "ACTIVE_DEVICES", "ACTIVE_FILTER")]
        p['SKYQUALITY'] = [self.get_text(self.driver, "ACTIVE_DEVICES", "ACTIVE_SKYQUALITY")]
        return p
                    
    @property
    def activedevicetelescope(self):
        """
        Return ACTIVE_DEVICES ACTIVE_TELESCOPE, return astropy table
        """
        p = Table()
        p['TELESCOPE'] = [self.get_text(self.driver, "ACTIVE_DEVICES", "ACTIVE_TELESCOPE")]
        return p

    @activedevicetelescope.setter
    def activedevicetelescope(self,string):
        """
        Set ACTIVE_DEVICES ACTIVE_TELESCOPE
        """
        self.set_and_send_text(self.driver, 'ACTIVE_DEVICES', 'ACTIVE_TELESCOPE', string)

    @property
    def activedevicerotator(self):
        """
        Return ACTIVE_DEVICES ACTIVE_FOCUSER, return astropy table
        """
        p = Table()
        p['ROTATOR'] = [self.get_text(self.driver, "ACTIVE_DEVICES", "ACTIVE_ROTATOR")]
        return p

    @activedevicerotator.setter
    def activedevicerotator(self,string):
        """
        Set ACTIVE_DEVICES ACTIVE_ROTATOR
        """
        self.set_and_send_text(self.driver, 'ACTIVE_DEVICES', 'ACTIVE_ROTATOR', string)
    
    @property
    def activedevicefocuser(self):
        """
        Return ACTIVE_DEVICES ACTIVE_FOCUSER, return astropy table
        """
        p = Table()
        p['FOCUSER'] = [self.get_text(self.driver, "ACTIVE_DEVICES", "ACTIVE_FOCUSER")]
        return p
 
    @activedevicefocuser.setter
    def activedevicefocuser(self,string):
        """
        Set ACTIVE_DEVICES ACTIVE_FOCUSER
        """
        self.set_and_send_text(self.driver, 'ACTIVE_DEVICES', 'ACTIVE_FOCUSER', string)

    @property
    def activedevicefilter(self):
        """
        Return ACTIVE_DEVICES ACTIVE_FILTER, return astropy table
        """
        p = Table()
        p['FILTER'] = [self.get_text(self.driver, "ACTIVE_DEVICES", "ACTIVE_FILTER")]
        return p
 
    @activedevicefilter.setter
    def activedevicefilter(self,string):
        """
        Set ACTIVE_DEVICES ACTIVE_FILTER
        """
        self.set_and_send_text(self.driver, 'ACTIVE_DEVICES', 'ACTIVE_FILTER', string)

   
    @property
    def activedeviceskyquality(self):
        """
        Return ACTIVE_DEVICES ACTIVE_SKYQUALITY, return astropy table
        """
        p = Table()
        p['SKYQUALITY'] = [self.get_text(self.driver, "ACTIVE_DEVICES", "ACTIVE_SKYQUALITY")]
        return p
       
        
    @activedeviceskyquality.setter
    def activedeviceskyquality(self,string):
        """
        Set ACTIVE_DEVICES ACTIVE_SKYQUALITY
        """
        self.set_and_send_text(self.driver, 'ACTIVE_DEVICES', 'ACTIVE_SKYQUALITY', string)

