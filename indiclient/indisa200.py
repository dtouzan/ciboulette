# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with sa200 via the INDI protocol, http://www.indilib.org.
"""

import time
import os
import io
import socket
socket.gethostname()

import logging
import logging.handlers

from .indiclient import indiclient

log = logging.getLogger("")
log.setLevel(logging.INFO)

class SA200Motor(indiclient):
    """
    Wrap indiclient.indiclient with some filter-specific utility functions to simplify things like taking,
    filters, filter name, etc.
    """
    def __init__(self, host, port, driver="SA200", debug=True):
        super(SA200Motor, self).__init__(host, port)
        self.filter_name = "SA200"
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
    def initialization(self):
        self.slot_value = "1"
        self.degree = "0"
        self.R = "200"
        self.length = "20"
        self.hostname = socket.gethostname()
        self.PID = os.getppid()
        return True
    
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
    def slots(self):
        """
        Return list of names of installed filters
        """
        slots_list = [e.get_text() for e in self.get_vector(self.driver, "FILTER_NAME").elements]
        return slots_list

    @property
    def slot_value(self):
        slot_value = int(self.get_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE"))  # filter slots 1-indexed
        return slot_value

    @slot_value.setter
    def slot_value(self, f):
        self.set_and_send_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE", f)
        return f

    @property
    def driver_name(self):
        """
        Return driver_name
        """
        name = self.get_text(self.driver, "DRIVER_INFO", "DRIVER_NAME")
        return name   
                
    def connect(self):
        """
        Enable sa200 connection
        """
        vec = self.set_and_send_switchvector_by_elementlabel(self.driver, "CONNECTION", "Connect")
        if self.debug and vec is not None:
            vec.tell()
        self.process_events()
        return vec

    def disconnect(self):
        """
        Disable sa200 connection
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
    def degree(self):
        """
        Return info of slot 1
        """
        text = self.get_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_1")
        return text
    
    @degree.setter
    def degree(self, string):      
        """Initialization slots 1
            reserved : length
        """
        self.set_and_send_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_1", string)
        return 
    
    @property
    def R(self):
        """
        Return info of slot 2
        """
        text = self.get_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_2")
        return text
    
    @R.setter
    def R(self, string):      
        """Initialization slots 2
            reserved : R200
        """
        self.set_and_send_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_2", string)
        return 

    @property
    def length(self):
        """
        Return info of slot 2
        """
        text = self.get_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_3")
        return text
    
    @length.setter
    def length(self, string):      
        """Initialization slots 3
            reserved : length
        """
        self.set_and_send_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_3", string)
        return True

    @property
    def hostname(self):
        """
        Return info of slot 4
        """
        text = self.get_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_4")
        return text
    
    @hostname.setter
    def hostname(self, string):      
        """Initialization slots 4 
            reserved : Hostname
        """
        if self.hostname == "0" : 
            self.set_and_send_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_4", string) 
    
    @property
    def software(self):
        """
        Return info of slot 5
        """
        text = self.get_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_5")
        return text
    
    @software.setter
    def software(self, string):      
        """Initialization slots 5 
            reserved : software
        """
        self.set_and_send_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_5", string)
        return True  

    @property
    def PID(self):      
        """Get os process software 
        """
        text = self.get_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_6")
        return text

    @PID.setter
    def PID(self,pid):      
        """Set os process software 
            reserved : PID process
        """
        self.set_and_send_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_6", str(pid) )
        return True

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

    @property
    def ID(self):      
        """Return ID
            reserved : hostname:driver_name:software:PID
        """
        h = self.hostname
        d = self.driver_name
        s = self.software
        p = self.PID
        id = d+"@"+h+":"+s+":"+p
        return id

    @property
    def datastream(self):      
        """Return datastream json format
        """ 
        objet = '"' + self.driver_name + '":[{'
        slot = '"slot":' + '"' + str(self.slot_value) + '", '
        degree = '"degree":' + '"' + self.degree + '", '
        r = '"R":' + '"' + self.R + '", '
        length = '"length":' + '"' + self.length + '"}]'
        data = "{"+objet+slot+degree+r+length+"}"
        return data
