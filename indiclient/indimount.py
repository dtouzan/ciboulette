# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with mount a the INDI protocol, http://www.indilib.org.
"""

import time
import io

import logging
import logging.handlers

from astropy.io import fits
from astropy.table import Table

from .indiclient import indiclient

log = logging.getLogger("")
log.setLevel(logging.INFO)

class Telescope(indiclient):
    """
    Wrap indiclient.indiclient with some filter-specific utility functions to simplify things like taking,
    mount, etc.
    """
    def __init__(self, host, port, driver="Mount Simulator", debug=True):
        super(Telescope, self).__init__(host, port)
        self.mount_name = "Mount Default"
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
    
    @property
    def sitelatitude(self):
        """
        Latitude initialization
        """
        self.process_events()
        f = self.get_float(self.driver, "GEOGRAPHIC_COORD", "LAT")
        return f

    @property
    def sitelongitude(self):
        """
        Latitude initialization
        """
        self.process_events()
        f = self.get_float(self.driver, "GEOGRAPHIC_COORD", "LONG")
        return f
 
    @property
    def siteelevation(self):
        """
        Latitude initialization
        """
        self.process_events()
        f = self.get_float(self.driver, "GEOGRAPHIC_COORD", "ELEV")
        return f

    @sitelatitude.setter
    def sitelatitude(self,f):
        """
        Latitude initialization
        """
        if f >=0 and f <=90:
            self.set_and_send_float(self.driver, "GEOGRAPHIC_COORD", "LAT", f)

    @sitelongitude.setter
    def sitelongitude(self,f):
        """
        Latitude initialization
        """
        if f >= -360 and f <= 360:
            self.set_and_send_float(self.driver, "GEOGRAPHIC_COORD", "LONG", f)
        
    @siteelevation.setter
    def siteelevation(self,f):
        """
        Latitude initialization
        """
        if f >= 0:
            self.set_and_send_float(self.driver, "GEOGRAPHIC_COORD", "ELEV", f)
            
    @property
    def parking(self):
        """
        Turn park on
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "TELESCOPE_PARK", "Park(ed)")
        if self.debug:
            vec.tell()
        return vec
    
    @property    
    def unpark(self):
        """
        Turn unpark on
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "TELESCOPE_PARK", "UnPark(ed)")
        if self.debug:
            vec.tell()
        return vec
    
    @property
    def tracking(self):
        """
        Turn track on
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "TELESCOPE_TRACK_STATE", "On")
        if self.debug:
            vec.tell()
        return vec
    
    @property    
    def untrack(self):
        """
        Turn untrack on
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "TELESCOPE_TRACK_STATE", "Off")
        if self.debug:
            vec.tell()
        return vec
    
    @property
    def utc(self):
        """
        Return UTC format
        Ex : 2021-02-19T22:00:00
        """
        string = self.get_text(self.driver, "TIME_UTC", "UTC")
        return string
    
    @utc.setter
    def utc(self,string):
        """
        Set UTC format
        Ex : '2021-02-19T22:00:00'
        """
        self.set_and_send_text(self.driver, "TIME_UTC", "UTC", string)

    @property
    def offset(self):
        """
        Return OFFSET 
        """
        f = self.get_text(self.driver, "TIME_UTC", "OFFSET")
        return f
    
    @offset.setter
    def offset(self,f):
        """
        Set OFFSET 
        """
        self.set_and_send_float(self.driver, "TIME_UTC", "OFFSET", f)

    @property
    def telescope_pier_side(self):
        """
        Return TELESCOPE_PEIR_SIDE : read_only, return astropy table
        """
        p = Table()
        p['WEST'] = [self.get_text(self.driver, "TELESCOPE_PIER_SIDE", "PIER_WEST")]
        p['EAST'] = [self.get_text(self.driver, "TELESCOPE_PIER_SIDE", "PIER_EAST")]
        return p

    @property
    def target_pier_side(self):
        return None

    @target_pier_side.setter
    def target_pier_side(self,string):
        """
        Set TARGET_PEIR_SIDE Auto, East (pointing west), West (pointing east)
        """ 
        if string in ('A','E','W'):
            if string =='A':
                vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "TARGETPIERSIDE", "Auto")
            if string =='E':
                vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "TARGETPIERSIDE", "East (pointing west)")
            if string =='W':
                vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "TARGETPIERSIDE", "West (pointing east)")
                
    @property
    def telescope_park_position(self):
        """
        Return TELESCOPE_PARK_POSITION in astropy table
        """
        p = Table()
        p['RA'] = [self.get_float(self.driver, "TELESCOPE_PARK_POSITION", "PARK_RA")]
        p['DEC'] = [self.get_float(self.driver, "TELESCOPE_PARK_POSITION", "PARK_DEC")]
        return p

    @property
    def on_coord_set(self):
        """
        Return ON_COORD_SET in astropy table
        """
        p = Table()
        p['TRACK'] = [self.get_text(self.driver, "ON_COORD_SET", "TRACK")]
        p['SLEW'] = [self.get_text(self.driver, "ON_COORD_SET", "SLEW")]
        p['SYNC'] = [self.get_text(self.driver, "ON_COORD_SET", "SYNC")]
        return p

    @on_coord_set.setter
    def on_coord_set(self,label):
        """
        Set ON_COORD_SET to Track, Slew or Sync
        """
        if label in ('Track','Slew','Sync'):             
                vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "ON_COORD_SET", label)       
                if self.debug:
                    vec.tell() 

    def synctocoordinates(self,ra,dec):
        """
        Synchronizes the telescope positions with the initialized coordinates
        ra (float): HH.HHHHHH
        dec (float): DD.DDDDDD
        """
        if ra >= 0 and ra < 24:
            if dec >= -90 and dec <=90:
                self.tracking
                self.on_coord_set = 'Sync'
                string = str(ra)
                self.set_and_send_text(self.driver, 'EQUATORIAL_EOD_COORD', 'RA', string)
                string = str(dec)
                self.set_and_send_text(self.driver, 'EQUATORIAL_EOD_COORD', 'DEC', string)
        self.on_coord_set = 'Track'
 
    def slewtocoordinates(self,ra,dec):
        """
        Slew the telescope positions with the initialized coordinates
        ra (float): HH.HHHHHH
        dec (float): DD.DDDDDD
        """
        if ra >= 0 and ra < 24:
            if dec >= -90 and dec <=90:
                self.tracking                  
                self.on_coord_set = 'Track'
                self.unpark
                vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "TELESCOPE_SLEW_RATE", '32x')       
                if self.debug:
                    vec.tell()               
                sra = str(ra)
                self.set_and_send_text(self.driver, 'EQUATORIAL_EOD_COORD', 'RA', sra)
                sdec = str(dec)
                self.set_and_send_text(self.driver, 'EQUATORIAL_EOD_COORD', 'DEC', sdec)    
                  
    @property
    def telescope_track_mode(self):
        """
        Return TELESCOPE_TRACK_MODE mode, return astropy table
        """
        p = Table()
        p['SIDEREAL'] = [self.get_text(self.driver, "TELESCOPE_TRACK_MODE", "TRACK_SIDEREAL")]
        p['LUNAR'] = [self.get_text(self.driver, "TELESCOPE_TRACK_MODE", "TRACK_LUNAR")]
        p['SOLAR'] = [self.get_text(self.driver, "TELESCOPE_TRACK_MODE", "TRACK_SOLAR")]
        p['CUSTOM'] = [self.get_text(self.driver, "TELESCOPE_TRACK_MODE", "TRACK_CUSTOM")]
        return p
                    
    @telescope_track_mode.setter
    def telescope_track_mode(self,label):
        """
        Set TELESCOPE_TRACK_MODE. Sideral, Lunar, Solar, Custom
        """
        if label in ('Sideral','Lunar','Solar','Custom'):
            vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "TELESCOPE_TRACK_MODE", label)       
            if self.debug:
                vec.tell()               
            
