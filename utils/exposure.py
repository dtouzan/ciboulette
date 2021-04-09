"""
Exposure class
"""

from datetime import datetime

class Exposure(object):
    
    def __init__(self):
        self.datatype = 'Intensity'
        self.exptime = 0
        self.label = 1       

    @property
    def exp_time(self):
        """
        Return exposure time                  
        """         
        return self.exptime
    
    @property
    def exp_label(self):
        """
        Return label of frame
        """
        return self.label

    @exp_time.setter
    def exp_time(self,exptime):
        """
        Initialization exposure time
        exptime (float): Exposure time second.
        """                    
        self.exptime = exptime            

    @exp_label.setter  
    def exp_label(self,label):
        """
        Initialization serial label
         label (int): Serial label.
        """
        self.label = label

    @property    
    def inc_label(self):
        """
        Increment serial label
        """
        self.label = self.label + 1
     
    @property
    def today_to_label(self):
        """
        Initialization serial label whit date end time                         
        """
        today = datetime.today()        
        self.label = today.strftime('%Y%m%d%H%M%S')
