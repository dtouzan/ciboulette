# Licensed under GPL3 (see LICENSE)
# coding=utf-8

"""
Classes and utility functions for communicating with sa200 via the INDI protocol, http://www.indilib.org.
"""

import time
import os
import io
import socket

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
        self.set_slot_value("4")
        self.set_R("200")
        self.set_length("20.5")
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

    def get_blocks(self):
        """
        Return list of names of installed filters
        """
        slots_list = [e.get_text() for e in self.get_vector(self.driver, "FILTER_NAME").elements]
        return slots_list

    def get_slot_value(self):
        slot_value = int(self.get_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE"))  # filter slots 1-indexed
        return slot_value
    
    def motor(self):
        self.set_and_send_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE", 1)           
        return self.get_degree()


    def motor_out(self): 
        self.set_degree('0')
        return self.get_degree()
      
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
    
    def get_block(self,slot):
        """
        Return info of slot number
        """
        text = ""
        if slot > 0 and slot < 11 :
            text = self.get_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_"+str(slot))
        return text
    
    def set_block(self, slot, string):      
        """Initialization slot 4 to 10
        """
        if slot > 4 and slot < 11 :
            self.set_and_send_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_"+str(slot), string)
        else:
            return False   

    def get_degree(self):
        """
        Return info of slot 1
        """
        text = self.get_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_1")
        return text
    
    def set_degree(self, string):      
        """Initialization slots 1
            reserved : -360° to 360°
        """
        self.set_and_send_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_1", string)
        self.set_and_send_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE", 1) 
        return True

        
    def get_R(self):
        """
        Return info of slot 2
        """
        text = self.get_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_2")
        return text
    
    def set_R(self, string):      
        """Initialization slots 2
            reserved : R200
        """
        self.set_and_send_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_2", string)
        self.set_and_send_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE", 2) 
        return True

    def get_length(self):
        """
        Return info of slot 3
        """
        text = self.get_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_3")
        return text
    
    def set_length(self, string):      
        """Initialization slots 3
            reserved : length
        """
        self.set_and_send_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_3", string)
        self.set_and_send_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE", 3)
        return True

    def get_speed(self):
        """
        Return info of slot 4
        """
        text = self.get_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_4")
        return text
    
    def set_speed(self, string):      
        """Initialization slots 4
            reserved : length
        """
        self.set_and_send_text(self.driver, "FILTER_NAME", "FILTER_SLOT_NAME_4", string)
        self.set_and_send_float(self.driver, "FILTER_SLOT", "FILTER_SLOT_VALUE", 4)
        return True
   
    
    def load(self):      
        """Load indilid configuration file .xml
        """
        self.set_and_send_text(self.driver, "CONFIG_PROCESS", "CONFIG_LOAD", "On")
        return True

    def save(self):      
        """Save indilid configuration file .xml
        """
        self.set_and_send_text(self.driver, "CONFIG_PROCESS", "CONFIG_SAVE", "On")
        return True 

    def datastream(self):      
        """Return datastream json format
        """ 
        name = ' "SA200":'
        value = '{ "value":' + '"' + str(self.get_slot_value()) + '", '
        degrees = '"degree":' + '"' + self.get_degree() + '", '          
        r = '"R":' + '"' + self.get_R() + '", '
        length = '"length":' + '"' + self.get_length() + '", '
        speed = '"speed":' + '"' + self.get_speed() + '", '     
        slot5 = '"block05":' + '"' + self.get_block(5) + '", '
        slot6 = '"block06":' + '"' + self.get_block(6) + '", '
        slot7 = '"block07":' + '"' + self.get_block(7) + '", '
        slot8 = '"block08":' + '"' + self.get_block(8) + '", '
        slot9 = '"block09":' + '"' + self.get_block(9) + '", '
        slot10 = '"block10":' + '"' + self.get_block(10) + '" '
        
        data = "{"+name+value+degrees+r+length+speed+slot5+slot6+slot7+slot8+slot9+slot10+"} }"
        return data
