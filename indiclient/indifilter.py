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

log = logging.getLogger("")
log.setLevel(logging.INFO)


class FILTERWheel(indiclient):
    """
    Wrap indiclient.indiclient with some filter-specific utility functions to simplify things like taking,
    filters, filter name, etc.
    """
    def __init__(self, host, port, driver="Filter Simulator", debug=True):
        super(FILTERWheel, self).__init__(host, port)
        self.filter_name = "Filter" Default"
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

    @property
    def filters(self):
        """
        Return list of names of installed filters
        """
        filters = [e.get_text() for e in self.get_vector(self.driver, "FILTER_NAME").elements]
        return filters

    @property
    def filter(self):
        slot = int(self.get_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE"))  # filter slots 1-indexed
        return slot

    @filter.setter
    def filter(self, f):
        if isinstance(f, int):
            if f >= 0 and f < len(self.filters):
                self.set_and_send_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE", f+1)
        else:
            if f in self.filters:
                self.set_and_send_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE", self.filters.index(f)+1)

    @property
    def filtername(self):
        """
        Return name of filter selected
        """
        slot = self.filter
        if slot >= 0 and slot <= len(self.filters):
            f = self.filters[slot-1]
        else:
            f = None
        return f
    
    @filtername.setter
    def filtername(self, string):      
        """Initialization filters name
            Ex: 'Blue'
        Attributes:
            filters (string): Name filter.
        """
        if string in self.filters:
            filters = self.filters
            self.filter = filters.index(string)        

    @property
    def filternames(self):
        """
        Return list of names of installed filters
        """
        return self.filters

    @filternames.setter
    def filternames(self, name_list):
        """Initialization filters table
            Ex: ['B','Ha','H_alpha', etc]
        Attributes:
            filters (list): Name filters list.
        """
        slot = 1
        if len(name_list) > 0:
            for name in name_list:
                self.set_and_send_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_"+str(slot), name)
                slot +=1
            
                
    def connect(self):
        """
        Enable filterwheel connection
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "CONNECTION", "Connect")
        if self.debug and vec is not None:
            vec.tell()
        self.process_events()
        return vec

    def disconnect(self):
        """
        Disable filterwheel connection
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
